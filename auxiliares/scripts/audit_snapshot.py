#!/usr/bin/env python3
"""Auditoria opcional, somente leitura, de uma copia estavel do vault schema 2."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import re

IGNORE = {'.git', '.obsidian', '.venv', '__pycache__'}
NOTE_ROOTS = ('00-Inbox/', '01-Diario/', '02-Tarefas/', '03-Projetos/',
              '04-Areas/', '05-Conhecimento/', '06-Rotinas/', '07-Recursos/',
              '08-Sistema/Perfis/', '08-Sistema/Decisoes/', '08-Sistema/Objetivos/',
              '08-Sistema/Fontes/', '08-Sistema/Modulos/',
              '99-Arquivo/Tarefas/', '99-Arquivo/Projetos/')
STATES = {
 'captura': ['Nova', 'Processada', 'Descartada'],
 'tarefa': ['Inbox', 'Próxima ação', 'Em andamento', 'Aguardando', 'Bloqueada', 'Algum dia', 'Concluído', 'Cancelado'],
 'projeto': ['Backlog', 'Ativo', 'Pausado', 'Concluído', 'Cancelado'],
 'area': ['Ativa', 'Inativa'], 'objetivo': ['Proposto', 'Ativo', 'Pausado', 'Alcançado', 'Cancelado'],
 'rotina': ['Rascunho', 'Ativa', 'Pausada', 'Desativada'],
 'conhecimento': ['Rascunho', 'Vigente', 'A revisar', 'Superado'],
 'recurso': ['Disponível', 'Indisponível', 'Arquivado'], 'registro': ['Registrado', 'Corrigido'],
 'decisao': ['Proposta', 'Vigente', 'Substituída', 'Revogada'],
 'perfil': ['Em descoberta', 'Vigente', 'A revisar'],
 'fonte': ['Não verificada', 'Disponível', 'Limitada', 'Indisponível', 'Revogada'],
 'modulo': ['Proposto', 'Piloto', 'Ativo', 'Pausado', 'Desativado']}
COMMON = 'id schema_version tipo titulo status criado atualizado origem confianca sensibilidade'.split()
LISTS = ('objetivo_ids fontes modulos aliases tags evidencias dependencias destino_ids '
         'contextos substitui_ids escopo_ids dependencias_modulo autoridade_sobre').split()
FIELDS = set((' '.join(COMMON) + ' ' + ' '.join(LISTS) + ' ' +
 'origem_ref area_id projeto_id chave_origem prioridade prioridade_origem prazo prazo_em '
 'prazo_origem_ref revisar_em duracao_min estimativa_origem energia aguardando '
 'criterio_aceite concluido cancelado motivo_cancelamento resultado proxima_acao_id '
 'condicao_retomada responsabilidade criterio_manutencao horizonte indicador valor_atual '
 'verificado_em gatilho timezone agenda_ref disparador_ref agendamento_status janela_min '
 'politica_atraso max_tentativas canal_entrega_ref versao_procedimento pergunta validade '
 'local_ref versao_ref licenca_ref categoria data periodo_inicio periodo_fim rotina_id '
 'chave_execucao estado_execucao tentativa executor_ref resultado_status entrega_status '
 'vigente_desde motivo confirmado_em conexao_ref capacidade_ref frescor_max_min slug '
 'versao_modulo manifesto_ref necessidade_ref').split())
RELATIONS = {'area_id':'area', 'projeto_id':'projeto', 'rotina_id':'rotina',
             'proxima_acao_id':'tarefa', 'objetivo_ids':'objetivo', 'fontes':'fonte',
             'modulos':'modulo', 'dependencias':'tarefa', 'substitui_ids':'decisao',
             'dependencias_modulo':'modulo', 'destino_ids':None, 'escopo_ids':None}


def strict_json(text):
    def reject(value):
        raise ValueError('constante JSON nao finita')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError('chave JSON repetida')
            result[key] = value
        return result
    return json.loads(text, parse_constant=reject, object_pairs_hook=unique)


def safe_relative(name):
    if not isinstance(name, str) or not name or name.startswith('/') or '\\' in name or ':' in name or '\x00' in name:
        raise ValueError('caminho invalido')
    if any(ord(c)<32 or c in '<>"|?*' for c in name): raise ValueError('caractere de caminho invalido')
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{p}{i}' for p in ('COM', 'LPT') for i in range(1, 10)}
    parts = name.split('/')
    if any(p in ('', '.', '..') or p.endswith((' ', '.')) or p.split('.')[0].upper() in reserved for p in parts):
        raise ValueError('caminho nao portavel')
    return parts


def is_link(path):
    """Inclui junctions/reparse points do Windows, sem exigir Python 3.12."""
    path = Path(path)
    try: return path.is_symlink() or bool(getattr(path.lstat(), 'st_reparse_tag', 0))
    except FileNotFoundError: return False


def regular_files(root):
    root = Path(root)
    if is_link(root) or not root.is_dir():
        raise ValueError('origem deve ser diretorio real')
    selected = []
    def walk(folder):
        for p in sorted(folder.iterdir()):
            rel = p.relative_to(root)
            if any(part in IGNORE for part in rel.parts):
                continue
            if is_link(p):
                raise ValueError('symlink nao permitido: ' + rel.as_posix())
            safe_relative(rel.as_posix())
            if p.is_dir(): walk(p)
            elif p.is_file(): selected.append(p)
            else: raise ValueError('arquivo especial nao permitido')
            if len(selected) > 20000: raise ValueError('limite de arquivos excedido')
    walk(root)
    return selected


def parse_note(data):
    text = data.decode('utf-8-sig').replace('\r\n', '\n')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError('frontmatter ausente')
    head, body = text[4:].split('\n---\n', 1)
    meta = {}
    for line in head.splitlines():
        if not line.strip(): continue
        key, sep, value = line.partition(':')
        if not sep or not re.fullmatch(r'[a-z][a-z0-9_]*', key) or key in meta:
            raise ValueError('chave invalida ou repetida')
        val = strict_json(value.strip())
        if isinstance(val, dict) or (isinstance(val, list) and any(isinstance(x, (dict, list)) for x in val)):
            raise ValueError('frontmatter aninhado nao permitido')
        meta[key] = val
    return meta, body


def stamp(value):
    try: parsed = dt.datetime.fromisoformat(value)
    except (ValueError, TypeError): raise ValueError('timestamp invalido') from None
    if parsed.tzinfo is None: raise ValueError('timestamp sem offset')
    return parsed


def validate(meta):
    if any(k not in meta for k in COMMON): raise ValueError('campo comum ausente')
    if not isinstance(meta['id'], str) or not re.fullmatch(r'n_[0-9a-f]{32}', meta['id']): raise ValueError('ID invalido')
    if type(meta['schema_version']) is not int or meta['schema_version'] != 2: raise ValueError('schema nao suportado')
    kind = meta['tipo']
    if not isinstance(kind, str) or kind not in STATES or meta['status'] not in STATES[kind]: raise ValueError('tipo/status invalido')
    if any(not isinstance(meta[k], str) or not meta[k].strip() for k in ('titulo', 'origem')): raise ValueError('titulo/origem vazio')
    if meta['confianca'] not in ('confirmado', 'inferido', 'nao_verificado'): raise ValueError('confianca invalida')
    if meta['sensibilidade'] not in ('publico', 'pessoal', 'restrito'): raise ValueError('sensibilidade invalida')
    if stamp(meta['atualizado']) < stamp(meta['criado']): raise ValueError('atualizacao anterior a criacao')
    for key, value in meta.items():
        if key not in FIELDS and not re.fullmatch(r'mod_[a-z0-9_]+__[a-z0-9_]+', key): raise ValueError('campo nao registrado: ' + key)
        if isinstance(value, float) and not math.isfinite(value): raise ValueError('numero nao finito')
    for key in LISTS:
        if key in meta and (not isinstance(meta[key], list) or any(not isinstance(x, str) or not x.strip() for x in meta[key])):
            raise ValueError('lista de strings esperada: ' + key)
        if key in meta and len(meta[key]) != len(set(meta[key])): raise ValueError('lista repetida: ' + key)
    for key in ('prazo','revisar_em','concluido','cancelado','data','periodo_inicio','periodo_fim'):
        if meta.get(key) is not None:
            try:
                if not isinstance(meta[key], str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',meta[key]): raise ValueError()
                dt.date.fromisoformat(meta[key])
            except (ValueError,TypeError): raise ValueError('data civil invalida: ' + key) from None
    for key in ('chave_execucao','chave_origem','slug','criterio_aceite','aguardando','motivo_cancelamento'):
        if meta.get(key) is not None and (not isinstance(meta[key],str) or not meta[key].strip()):
            raise ValueError('string nao vazia esperada: ' + key)
    for key in ('prazo_em','verificado_em','vigente_desde','confirmado_em'):
        if meta.get(key) is not None: stamp(meta[key])
    if meta.get('prioridade') not in (None, 'P1', 'P2', 'P3'): raise ValueError('prioridade invalida')
    if meta.get('duracao_min') is not None and (type(meta['duracao_min']) is not int or meta['duracao_min'] < 1): raise ValueError('duracao invalida')
    if kind in ('tarefa','projeto'):
        state = meta['status']
        if state == 'Concluído' and (not meta.get('concluido') or not meta.get('criterio_aceite') or not meta.get('evidencias')):
            raise ValueError('conclusao sem data, aceite ou evidencia')
        if state == 'Cancelado' and (not meta.get('cancelado') or not meta.get('motivo_cancelamento')):
            raise ValueError('cancelamento sem data/motivo')
        if state != 'Concluído' and meta.get('concluido') is not None: raise ValueError('conclusao vigente em estado aberto/cancelado')
        if state != 'Cancelado' and meta.get('cancelado') is not None: raise ValueError('cancelamento vigente em outro estado')
    if kind == 'tarefa' and meta['status'] == 'Aguardando' and not meta.get('aguardando'): raise ValueError('espera sem contexto')
    if kind == 'rotina' and meta['status'] == 'Ativa':
        if not meta.get('criterio_aceite'): raise ValueError('rotina ativa sem aceite')
        if meta.get('gatilho') not in ('sob_demanda','agendado_app','automacao_nuvem'): raise ValueError('gatilho invalido')
        if meta['gatilho'] != 'sob_demanda' and (not meta.get('timezone') or not meta.get('agenda_ref') or not meta.get('disparador_ref') or meta.get('agendamento_status') != 'ativo'):
            raise ValueError('rotina agendada sem configuracao verificada declarada')
    if kind == 'captura' and meta['status'] == 'Processada' and not meta.get('destino_ids'):
        raise ValueError('captura processada sem destino')


def is_derived_index(path):
    """Indice.md sem frontmatter e uma pagina derivada de navegacao."""
    path = Path(path)
    return path.name.casefold() == 'indice.md' and not path.read_text(encoding='utf-8-sig').startswith('---')


def audit(root):
    root = Path(root)
    errors, warnings, notes = [], [], {}
    def issue(path, rule): return {'path':path, 'rule':rule}
    try: files = regular_files(root)
    except (ValueError, OSError) as exc: return {'ok':False,'notes':0,'errors':[issue('.',str(exc))],'warnings':[]}
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.suffix != '.md' or not rel.startswith(NOTE_ROOTS): continue
        try:
            if path.stat().st_size > 1_048_576: raise ValueError('nota excede limite de auditoria')
            if is_derived_index(path): continue
            meta, _ = parse_note(path.read_bytes()); validate(meta)
            if meta['id'] in notes: raise ValueError('ID duplicado')
            notes[meta['id']] = (meta, rel)
        except (ValueError, TypeError, KeyError, OSError, UnicodeError) as exc:
            errors.append(issue(rel, str(exc)))
    unique = {}
    for ident, (m, rel) in notes.items():
        for field, expected_kind in RELATIONS.items():
            values = m.get(field, []) if field in LISTS else [m.get(field)]
            for target in values:
                if target is None: continue
                if not isinstance(target, str) or target not in notes:
                    errors.append(issue(rel, 'referencia ausente: ' + field)); continue
                if expected_kind and notes[target][0]['tipo'] != expected_kind:
                    errors.append(issue(rel, 'tipo de referencia incorreto: ' + field))
        for key in ('chave_execucao', 'chave_origem'):
            if not m.get(key): continue
            pair = (key, m[key])
            if pair in unique: errors.append(issue(rel, key + ' duplicada'))
            unique[pair] = ident
        if m['tipo'] == 'tarefa' and m['status'] in ('Próxima ação','Em andamento'):
            project = notes.get(m.get('projeto_id'))
            if project and project[0]['status'] != 'Ativo': warnings.append(issue(rel, 'excluir do foco: projeto inativo'))
        for field in m:
            match = re.fullmatch(r'mod_([a-z0-9_]+)__[a-z0-9_]+', field)
            if match and not any(notes.get(x, ({},''))[0].get('slug') == match[1] for x in m.get('modulos', [])):
                errors.append(issue(rel, 'namespace sem modulo relacionado'))
    for field in ('dependencias','substitui_ids','dependencias_modulo'):
        visiting, done = set(), set()
        def visit(ident):
            if ident in visiting: raise ValueError('ciclo em ' + field)
            if ident in done: return
            visiting.add(ident)
            for nxt in notes[ident][0].get(field, []):
                if isinstance(nxt, str) and nxt in notes: visit(nxt)
            visiting.remove(ident); done.add(ident)
        try:
            for ident in notes: visit(ident)
        except (ValueError, RecursionError) as exc: errors.append(issue('.',str(exc)))
    return {'ok':not errors,'notes':len(notes),'errors':errors,'warnings':warnings,
            'limitation':'auditoria estrutural parcial; nao comprova verdade, consentimento, modulo completo, IANA ou acesso remoto'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('snapshot')
    result = audit(p.parse_args().snapshot)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
