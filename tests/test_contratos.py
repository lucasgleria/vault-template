"""Cenários fictícios dos contratos; não equivalem à homologação de um agente em nuvem."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ferramentas'))
import validar as v


def meta(kind='tarefa', **fields):
    template=(ROOT/'08-Sistema/Templates'/f'{kind}.md').read_bytes()
    m,_=v.audit.parse_note(template)
    for key,value in list(m.items()):
        if isinstance(value,str) and '__' in value:
            m[key]='Exemplo fictício'
    m.update(id='n_'+uuid.uuid4().hex,titulo='Cenário fictício',criado='2026-10-29T12:00:00+00:00',
             atualizado='2026-10-29T12:00:00+00:00',origem='teste-ficticio',origem_ref='teste:ficticio')
    if kind=='registro': m['data']='2026-10-29'
    m.update(fields)
    return m


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema=json.loads((ROOT/'08-Sistema/Esquemas/nota.schema.json').read_text(encoding='utf-8'))

    def test_templates_can_be_filled_without_personal_defaults(self):
        for kind in v.audit.STATES:
            with self.subTest(kind=kind):
                v.contract(meta(kind),self.schema)

    def test_specialized_field_wrong_type_is_rejected(self):
        with self.assertRaises(ValueError): v.contract(meta(max_tentativas=True),self.schema)

    def test_missing_acceptance_is_rejected_for_open_task(self):
        m=meta();m.pop('criterio_aceite')
        with self.assertRaises(ValueError): v.contract(m,self.schema)

    def test_empty_acceptance_is_rejected_for_open_task(self):
        with self.assertRaises(ValueError): v.contract(meta(criterio_aceite=''),self.schema)

    def test_unknown_status_and_field_are_rejected(self):
        for m in (meta(status='Feito'),meta(progresso=70)):
            with self.assertRaises(ValueError): v.contract(m,self.schema)

    def test_completion_without_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            v.contract(meta(status='Concluído',concluido='2026-10-29',evidencias=[]),self.schema)

    def test_same_title_can_refer_to_different_periods(self):
        first,second=meta(),meta()
        self.assertNotEqual(first['id'],second['id'])
        v.contract(first,self.schema);v.contract(second,self.schema)

    def test_priority_never_overrides_paused_or_backlog_project(self):
        for state in ('Pausado','Backlog','Concluído','Cancelado'):
            p=meta('projeto',status=state)
            t=meta(status='Próxima ação',prioridade='P1',projeto_id=p['id'])
            self.assertEqual(v.structural_candidates({p['id']:p,t['id']:t}),[])

    def test_cancelled_dependency_does_not_unlock_task(self):
        dep=meta(status='Cancelado');task=meta(status='Próxima ação',dependencias=[dep['id']])
        self.assertEqual(v.structural_candidates({dep['id']:dep,task['id']:task}),[])

    def test_completed_dependency_and_active_project_allow_candidate(self):
        dep=meta(status='Concluído');p=meta('projeto',status='Ativo')
        task=meta(status='Próxima ação',projeto_id=p['id'],dependencias=[dep['id']])
        notes={x['id']:x for x in (dep,p,task)}
        self.assertEqual(v.structural_candidates(notes),[task['id']])
        self.assertEqual(v.structural_candidates(notes,blocked_ids=[task['id']]),[])

    def test_unknown_context_does_not_claim_availability(self):
        t=meta(status='Próxima ação',contextos=['computador'])
        self.assertEqual(v.structural_candidates({t['id']:t}),[])
        self.assertEqual(v.structural_candidates({t['id']:t},available_contexts=['computador']),[t['id']])

    def test_global_pause_allows_direct_request_but_no_automatic_run(self):
        r=meta('rotina',status='Ativa')
        self.assertTrue(v.routine_allowed(r,{'global_pause':True},requested=True))
        self.assertFalse(v.routine_allowed(r,{'global_pause':True}))

    def test_individual_pause_needs_explicit_exception(self):
        r=meta('rotina',status='Pausada')
        self.assertFalse(v.routine_allowed(r,{'global_pause':False},requested=True))
        self.assertTrue(v.routine_allowed(r,{'global_pause':False},requested=True,explicit_exception=True))
        self.assertEqual(r['status'],'Pausada')

    def test_draft_can_be_used_on_demand_and_disabled_cannot(self):
        self.assertTrue(v.routine_allowed(meta('rotina'),{'global_pause':True},requested=True))
        self.assertFalse(v.routine_allowed(meta('rotina',status='Desativada'),{'global_pause':False},requested=True))

    def test_written_routine_does_not_imply_schedule(self):
        self.assertFalse(v.routine_allowed(meta('rotina',status='Ativa'),{'global_pause':False}))

    def test_digest_is_order_independent_and_sensitive_to_bytes(self):
        a={'02-Tarefas/a.md':b'A\n','03-Projetos/b.md':b'B\n'}
        self.assertEqual(v.changes_digest(a),v.changes_digest(dict(reversed(list(a.items())))))
        self.assertNotEqual(v.changes_digest(a),v.changes_digest({**a,'02-Tarefas/a.md':b'A\r\n'}))
        self.assertNotEqual(v.changes_digest(a),v.changes_digest({**a,'03-Projetos/b.md':None}))

    def test_digest_rejects_path_escape(self):
        with self.assertRaises(ValueError): v.changes_digest({'../outside':b'x'})

    def test_legacy_remote_target_and_privacy_are_explicit(self):
        c=json.loads((ROOT/'08-Sistema/config.json').read_text())
        c.update(document_version='2.0.0',onboarding_status='em_descoberta',
                 vault_id='v_'+'1'*32,proprietario_ref='teste:responsavel',
                 perfil_id='n_'+'2'*32,repositorio={
                     'nome_com_proprietario':'exemplo/vault',
                     'branch_canonica':'principal','privado_confirmado':True})
        for key in ('nome','finalidade','destino','estrutura'):
            c.pop(key,None)
        schema=json.loads((ROOT/'08-Sistema/Esquemas/config.schema.json').read_text())
        v.contract(c,schema)
        c['repositorio']['privado_confirmado']=False
        with self.assertRaises(ValueError): v.contract(c,schema)

    def test_new_template_validates_before_a_profile_exists(self):
        result=v.verify(ROOT)
        self.assertTrue(result['ok'],result['errors'])
        c=json.loads((ROOT/'08-Sistema/config.json').read_text())
        schema=json.loads((ROOT/'08-Sistema/Esquemas/config.schema.json').read_text())
        c['onboarding_status']='novo'
        for key in ('vault_id','proprietario_ref','perfil_id','repositorio','destino'):
            c[key]=None
        v.contract(c,schema)

    def test_configured_local_vault_requires_identity_and_purpose(self):
        c=json.loads((ROOT/'08-Sistema/config.json').read_text())
        schema=json.loads((ROOT/'08-Sistema/Esquemas/config.schema.json').read_text())
        c.update(onboarding_status='configurado',vault_id='v_'+'1'*32,
                 proprietario_ref='teste:responsavel',perfil_id='n_'+'2'*32,
                 nome='Coleção fictícia',finalidade='Organizar referências fictícias',
                 destino={'tipo':'pasta','referencia':'.'},
                 estrutura={'referencias':'05-Conhecimento/Referencias'})
        v.contract(c,schema)
        for key in ('vault_id','proprietario_ref','perfil_id','nome','finalidade','destino'):
            with self.subTest(key=key),self.assertRaises(ValueError):
                v.contract({**c,key:None},schema)
        c['destino']={'tipo':'git','referencia':'exemplo/vault'}
        with self.assertRaises(ValueError): v.contract(c,schema)

    def test_partial_setup_accepts_a_stable_identity_without_a_profile(self):
        c=json.loads((ROOT/'08-Sistema/config.json').read_text())
        schema=json.loads((ROOT/'08-Sistema/Esquemas/config.schema.json').read_text())
        c.update(onboarding_status='em_configuracao',vault_id='v_'+'1'*32,
                 destino={'tipo':'pasta','referencia':'.'})
        v.contract(c,schema)

    def test_configured_vault_checks_actual_collections_and_git_target(self):
        c=json.loads((ROOT/'08-Sistema/config.json').read_text())
        profile=meta('perfil')
        c.update(onboarding_status='configurado',vault_id='v_'+'1'*32,
                 proprietario_ref='teste:responsavel',perfil_id=profile['id'],
                 nome='Coleção fictícia',finalidade='Organizar referências fictícias',
                 destino={'tipo':'pasta','referencia':'.'},
                 estrutura={'referencias':'05-Conhecimento'})
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            schemas=root/'08-Sistema/Esquemas';schemas.mkdir(parents=True)
            for name in ('nota','config','operacao','modulo'):
                path=Path('08-Sistema/Esquemas')/(name+'.schema.json')
                (root/path).write_bytes((ROOT/path).read_bytes())
            profiles=root/'08-Sistema/Perfis';profiles.mkdir()
            head='\n'.join(key+': '+json.dumps(value,ensure_ascii=False) for key,value in profile.items())
            (profiles/(profile['id']+'.md')).write_text('---\n'+head+'\n---\nPerfil fictício.\n',encoding='utf-8')
            (root/'05-Conhecimento').mkdir()
            config_path=root/'08-Sistema/config.json'
            config_path.write_text(json.dumps(c),encoding='utf-8')
            self.assertTrue(v.verify(root)['ok'])
            index=root/'05-Conhecimento/Indice.md'
            index.write_text('# Referências\n\nColeção ainda vazia.\n',encoding='utf-8')
            result=v.verify(root)
            self.assertTrue(result['ok'],result['errors'])
            self.assertEqual(result['notes'],1)
            index.write_text('---\nid: "invalido"\n---\nÍndice com contrato inválido.\n',encoding='utf-8')
            self.assertFalse(v.verify(root)['ok'])
            index.write_text('# Referências\n',encoding='utf-8')
            for path in ('05-Conhecimento/Ausente','05-Conhecimento/../Fora'):
                c['estrutura']={'referencias':path}
                config_path.write_text(json.dumps(c),encoding='utf-8')
                self.assertFalse(v.verify(root)['ok'])
            c['estrutura']={}
            config_path.write_text(json.dumps(c),encoding='utf-8')
            self.assertFalse(v.verify(root)['ok'])
            c['estrutura']={'referencias':'05-Conhecimento'}
            c['destino']={'tipo':'git','referencia':'exemplo/outro'}
            c['repositorio']={'nome_com_proprietario':'exemplo/vault',
                              'branch_canonica':'principal','privado_confirmado':True}
            config_path.write_text(json.dumps(c),encoding='utf-8')
            self.assertFalse(v.verify(root)['ok'])
            c['destino']['referencia']='exemplo/vault'
            config_path.write_text(json.dumps(c),encoding='utf-8')
            self.assertTrue(v.verify(root)['ok'])

    def test_original_and_applied_auxiliary_hashes_are_distinguished(self):
        manifest=json.loads((ROOT/'auxiliares/manifesto.json').read_text())
        for name,info in manifest['files'].items():
            data=(ROOT/'auxiliares'/name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),info['sha256'])
            self.assertEqual(len(data),info['bytes'])

    @unittest.skipUnless(os.name=='nt','junction é específica do Windows')
    def test_windows_junction_is_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); target=root/'outside';target.mkdir()
            snapshot=root/'snapshot';snapshot.mkdir()
            link=snapshot/'redirect'
            result=subprocess.run(['cmd','/c','mklink','/J',str(link),str(target)],capture_output=True)
            if result.returncode: self.skipTest('junction indisponível no ambiente')
            try:
                self.assertTrue(v.audit.is_link(link))
                self.assertFalse(v.audit.audit(snapshot)['ok'])
            finally:
                # Remover somente o vínculo conhecido, nunca seu destino.
                os.rmdir(link)


if __name__=='__main__': unittest.main()
