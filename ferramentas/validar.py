"""Verificação opcional somente de leitura. Não escreve notas, chama API ou executa IA."""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import sys

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / 'auxiliares/scripts'))
import audit_snapshot as audit
import check_content


def contract(value, schema, path='$'):
    """Valida os keywords usados pelos contratos entregues; não é engine JSON Schema geral."""
    def fail(message):
        raise ValueError(path + ': ' + message)
    if 'const' in schema and value != schema['const']:
        fail('constante divergente')
    if 'enum' in schema and value not in schema['enum']:
        fail('enum inválido')
    kinds = schema.get('type', [])
    kinds = [kinds] if isinstance(kinds, str) else kinds
    actual = ('null' if value is None else 'boolean' if type(value) is bool else
              'integer' if type(value) is int else 'number' if type(value) is float else
              'string' if isinstance(value, str) else 'array' if isinstance(value, list) else 'object')
    if kinds and actual not in kinds and not (actual == 'integer' and 'number' in kinds):
        fail('tipo inválido')
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0):
            fail('string vazia')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            fail('formato inválido')
        if schema.get('format') == 'date-time':
            audit.stamp(value)
        if schema.get('format') == 'date':
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                fail('data inválida')
            dt.date.fromisoformat(value)
    if type(value) in (int, float):
        if not math.isfinite(value):
            fail('número não finito')
        if value < schema.get('minimum', -math.inf) or value > schema.get('maximum', math.inf):
            fail('número fora do limite')
    if isinstance(value, list):
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', math.inf):
            fail('quantidade de itens inválida')
        if schema.get('uniqueItems') and len({json.dumps(x,sort_keys=True) for x in value}) != len(value):
            fail('itens repetidos')
        for i, item in enumerate(value):
            contract(item, schema.get('items', {}), f'{path}[{i}]')
    if isinstance(value, dict):
        if any(k not in value for k in schema.get('required', [])):
            fail('campo obrigatório ausente')
        for key, item in value.items():
            schemas = []
            if key in schema.get('properties', {}):
                schemas.append(schema['properties'][key])
            schemas += [s for pattern, s in schema.get('patternProperties', {}).items() if re.search(pattern, key)]
            if not schemas and schema.get('additionalProperties') is False:
                fail('campo não registrado: ' + key)
            for child in schemas:
                contract(item, child, path + '.' + key)
    for child in schema.get('allOf', []):
        contract(value, child, path)
    if 'if' in schema:
        try:
            contract(value, schema['if'], path)
        except ValueError:
            contract(value, schema.get('else', {}), path)
        else:
            contract(value, schema.get('then', {}), path)


def changes_digest(changes):
    """O chamador seleciona caminhos de domínio; recibos/projeções ficam excluídos."""
    entries = {}
    for path, data in sorted(changes.items()):
        audit.safe_relative(path)
        entries[path] = None if data is None else hashlib.sha256(data).hexdigest()
    return hashlib.sha256(json.dumps(entries, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def structural_candidates(notes, blocked_ids=(), available_contexts=None):
    """Projeção estrutural; o agente ainda avalia decisões, capacidade e fontes atuais."""
    found = []
    for ident, meta in notes.items():
        if meta['tipo'] != 'tarefa' or meta['status'] not in ('Próxima ação', 'Em andamento') or ident in blocked_ids:
            continue
        if meta.get('projeto_id') and notes.get(meta['projeto_id'], {}).get('status') != 'Ativo':
            continue
        if any(notes.get(dep, {}).get('status') != 'Concluído' for dep in meta.get('dependencias', [])):
            continue
        contexts = set(meta.get('contextos', []))
        if contexts and (available_contexts is None or not contexts <= set(available_contexts)):
            continue
        found.append(ident)
    return sorted(found)


def routine_allowed(routine, config, *, requested=False, explicit_exception=False):
    if routine['status'] == 'Desativada':
        return False
    if routine['status'] == 'Pausada':
        return requested and explicit_exception
    if requested:
        return routine['status'] in ('Rascunho', 'Ativa')
    return (routine['status'] == 'Ativa' and not config['global_pause'] and
            routine.get('gatilho') in ('agendado_app', 'automacao_nuvem') and
            routine.get('agendamento_status') == 'ativo' and bool(routine.get('disparador_ref')))


def verify(root):
    root = Path(root)
    result = audit.audit(root)
    if not result['ok']:
        return result
    schemas = {name: audit.strict_json((root / '08-Sistema/Esquemas' / (name+'.schema.json')).read_text(encoding='utf-8'))
               for name in ('nota','config','operacao','modulo')}
    notes = {}
    def issue(path, rule):
        result['errors'].append({'path':path,'rule':rule})
    config = None
    for file in audit.regular_files(root):
        rel = file.relative_to(root).as_posix()
        if rel.startswith(('.runtime/', 'auxiliares/', 'tests/')):
            continue
        try:
            if file.suffix == '.md' and rel.startswith(audit.NOTE_ROOTS):
                if file.stat().st_size > 262144:
                    raise ValueError('nota excede 262144 bytes')
                if audit.is_derived_index(file):
                    continue
                meta, body = audit.parse_note(file.read_bytes())
                contract(meta, schemas['nota'])
                if re.search(r'__[A-Z][A-Z0-9_]*__', file.read_text(encoding='utf-8')):
                    raise ValueError('placeholder em nota aplicada')
                notes[meta['id']] = (meta, rel, body)
            elif file.suffix == '.json' and not rel.startswith('08-Sistema/Templates/'):
                value = audit.strict_json(file.read_text(encoding='utf-8'))
                if rel == '08-Sistema/config.json':
                    contract(value, schemas['config']); config = value
                elif rel.startswith('08-Sistema/Operacoes/'):
                    contract(value, schemas['operacao'])
                    if file.stem != value['operation_id']:
                        raise ValueError('caminho de recibo diverge do operation_id')
                elif rel.startswith('08-Sistema/Modulos/'):
                    contract(value, schemas['modulo'])
        except (ValueError, TypeError, OSError) as exc:
            issue(rel, str(exc))
    if config is None:
        issue('08-Sistema/config.json','configuração ausente ou inválida')
    elif config['perfil_id'] is not None and notes.get(config['perfil_id'], ({},))[0].get('tipo') != 'perfil':
        issue('08-Sistema/config.json','perfil ausente ou de tipo incorreto')
    if config is not None:
        destination = config.get('destino')
        if destination and destination['tipo'] == 'git':
            if destination['referencia'] != config['repositorio']['nome_com_proprietario']:
                issue('08-Sistema/config.json','destino diverge do repositório configurado')
        structure = config.get('estrutura', {})
        if config['onboarding_status'] == 'configurado' and not structure:
            issue('08-Sistema/config.json','vault configurado precisa de uma coleção')
        for path in structure.values():
            try:
                audit.safe_relative(path)
                if config['onboarding_status'] == 'configurado' and not (root / path).is_dir():
                    raise ValueError('coleção configurada sem diretório existente')
            except ValueError as exc:
                issue('08-Sistema/config.json',str(exc))
    for ident,(m,rel,body) in notes.items():
        if m['tipo'] == 'projeto' and m['status'] == 'Ativo':
            task = notes.get(m.get('proxima_acao_id'), ({},))[0]
            if task.get('tipo') != 'tarefa' or task.get('projeto_id') != ident:
                issue(rel,'projeto ativo precisa de próxima ação vinculada')
        if m['tipo'] == 'projeto' and m['status'] == 'Pausado' and not m.get('condicao_retomada') and 'pausa' not in body.casefold():
            issue(rel,'pausa precisa de motivo/contexto')
        if m['tipo'] == 'decisao' and m['status'] == 'Vigente' and (not m.get('vigente_desde') or not m.get('origem_ref')):
            issue(rel,'decisão vigente sem origem e vigência')
        if m['tipo'] == 'registro' and m.get('rotina_id'):
            if any(m.get(k) is None for k in ('chave_execucao','estado_execucao','tentativa','executor_ref','resultado_status','entrega_status')):
                issue(rel,'ocorrência sem contrato de execução completo')
        if m['tipo'] == 'modulo':
            manifest_ref = m.get('manifesto_ref')
            if m['status'] in ('Piloto','Ativo') and (not manifest_ref or not m.get('necessidade_ref')):
                issue(rel,'módulo em uso sem manifesto/necessidade')
            if manifest_ref:
                try:
                    audit.safe_relative(manifest_ref)
                    manifest = audit.strict_json((root/manifest_ref).read_text(encoding='utf-8'))
                    contract(manifest, schemas['modulo'])
                    if manifest['module_note_id'] != ident or manifest['module_slug'] != m['slug']:
                        raise ValueError('manifesto diverge da nota')
                except (ValueError, OSError) as exc:
                    issue(rel,str(exc))
        for key,value in m.items():
            if not key.startswith('mod_'):
                continue
            module = next((notes[x][0] for x in m.get('modulos',[]) if key.startswith('mod_'+notes[x][0].get('slug','')+'__')), None)
            try:
                if not module or not module.get('manifesto_ref'):
                    raise ValueError('campo de módulo sem manifesto aplicado')
                audit.safe_relative(module['manifesto_ref'])
                manifest = audit.strict_json((root/module['manifesto_ref']).read_text(encoding='utf-8'))
                definition = manifest['fields'].get(key)
                if not definition:
                    raise ValueError('campo não registrado no manifesto')
                field_schema={k:v for k,v in definition.items() if k in ('type','minimum','maximum')}
                if definition.get('nullable'):
                    field_schema['type']=[definition['type'],'null']
                contract(value,field_schema)
                if value is not None and definition.get('evidence_required_if_set') and not m.get('evidencias'):
                    raise ValueError('campo especializado sem evidência')
            except (ValueError,KeyError,OSError) as exc:
                issue(rel,str(exc))
    scan=check_content.check(root)
    result['content_scan']=scan
    result['errors'] += scan.get('findings',[])
    result['ok']=not result['errors']
    result['limitation']='Estrutura e contratos entregues; não comprova verdade, autorização, produto, agenda remota ou ausência completa de dados sensíveis.'
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', nargs='?',default='.')
    try:
        result=verify(parser.parse_args().snapshot)
    except (ValueError, OSError, KeyError) as exc:
        result={'ok':False,'errors':[{'rule':str(exc)}]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['ok'] else 1)
