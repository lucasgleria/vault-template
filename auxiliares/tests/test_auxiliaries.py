import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import audit_snapshot as audit
import check_content as content
import extract_bundle as bundle
import snapshot_archive as archive


def meta(kind='tarefa', number=1, **fields):
    m={'id':'n_'+f'{number:032x}','schema_version':2,'tipo':kind,'titulo':'Exemplo',
       'status':audit.STATES[kind][0],'criado':'2026-10-29T12:00:00+00:00',
       'atualizado':'2026-10-29T12:00:00+00:00','origem':'teste-ficticio',
       'confianca':'confirmado','sensibilidade':'pessoal'}
    m.update(fields); return m


def render(m,body='Texto de exemplo.\n'):
    return '---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in m.items())+'\n---\n\n'+body


def bundle_document(files):
    manifest={'version':'2.0.0','files':{}}
    blocks=[]
    for name,data in files.items():
        sha=hashlib.sha256(data).hexdigest()
        manifest['files'][name]={'sha256':sha,'bytes':len(data)}
        blocks.append('<!-- VAULT-FILE path='+name+' sha256='+sha+' -->\n````text\n'+data.decode()+'````\n<!-- END-VAULT-FILE -->')
    return '\n\n'.join(blocks)+'\n\n<!-- VAULT-MANIFEST version=2.0.0 -->\n````json\n'+json.dumps(manifest)+'\n````\n<!-- END-VAULT-MANIFEST -->\n'


class AuxiliaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
        self.root=self.base/'snapshot'; self.root.mkdir()
        self.put('08-Sistema/config.json',json.dumps({'schema_version':2,'global_pause':False}))
        self.put('AGENTS.md','# Regras ficticias\n')

    def tearDown(self): self.tmp.cleanup()

    def put(self,path,text):
        p=self.root/path; p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8'); return p

    def note(self,m,path=None):
        return self.put(path or '02-Tarefas/'+m['id']+'.md',render(m))

    def fails(self,m):
        self.note(m); self.assertFalse(audit.audit(self.root)['ok'])

    def make_archive(self):
        self.note(meta()); out=self.base/'copy.zip'; archive.create(self.root,out,'revision-ficticia'); return out

    def test_unicode_and_duplicate_titles_are_valid(self):
        self.note(meta(titulo='Saúde e educação')); self.note(meta(number=2,titulo='Saúde e educação'))
        self.assertTrue(audit.audit(self.root)['ok'])

    def test_missing_common_status(self):
        m=meta();m.pop('status');self.fails(m)

    def test_duplicate_frontmatter_key(self):
        with self.assertRaises(ValueError): audit.parse_note(render(meta()).replace('---\n\n','id: "outro"\n---\n\n').encode())

    def test_nested_frontmatter_rejected(self):
        m=meta();m['tags']={'unexpected':'value'}
        with self.assertRaises(ValueError): audit.parse_note(render(m).encode())

    def test_invalid_id(self): self.fails(meta(id='nome-mutavel'))
    def test_boolean_is_not_schema_integer(self): self.fails(meta(schema_version=True))
    def test_timezone_required_for_timestamp(self): self.fails(meta(criado='2026-10-29T12:00:00'))
    def test_update_before_creation(self): self.fails(meta(atualizado='2025-01-01T12:00:00+00:00'))
    def test_unknown_type(self): self.fails(meta(tipo='unknown'))
    def test_unknown_field(self): self.fails(meta(unregistered='x'))
    def test_invalid_duration_boolean(self): self.fails(meta(duracao_min=True))
    def test_compact_date_not_civil_contract(self): self.fails(meta(prazo='20261103'))
    def test_completion_requires_evidence(self): self.fails(meta(status='Concluído',concluido='2026-11-03',criterio_aceite='Entregue'))
    def test_completion_requires_date(self): self.fails(meta(status='Concluído',evidencias=['confirmação'],criterio_aceite='Entregue'))

    def test_legitimate_confirmation_can_close_without_fake_intermediate_states(self):
        self.note(meta(status='Concluído',concluido='2026-11-03',criterio_aceite='Entregue',evidencias=['canal:confirmacao-ficticia']))
        self.assertTrue(audit.audit(self.root)['ok'])

    def test_cancellation_requires_reason(self): self.fails(meta(status='Cancelado',cancelado='2026-11-03'))
    def test_cancel_is_not_completed(self): self.fails(meta(status='Cancelado',cancelado='2026-11-03',concluido='2026-11-03',motivo_cancelamento='Mudou'))
    def test_open_state_has_no_current_closure(self): self.fails(meta(concluido='2026-11-03'))
    def test_waiting_requires_context(self): self.fails(meta(status='Aguardando'))

    def test_duplicate_id_across_paths(self):
        self.note(meta());self.note(meta(),'02-Tarefas/outro.md');self.assertFalse(audit.audit(self.root)['ok'])

    def test_missing_reference(self): self.fails(meta(projeto_id='n_'+'f'*32))

    def test_reference_type_checked(self):
        self.note(meta(number=2));self.fails(meta(projeto_id='n_'+f'{2:032x}'))

    def test_dependency_cycle(self):
        self.note(meta(dependencias=['n_'+f'{2:032x}']));self.note(meta(number=2,dependencias=['n_'+f'{1:032x}']))
        self.assertFalse(audit.audit(self.root)['ok'])

    def test_decision_cycle(self):
        for i,j in ((1,2),(2,1)):
            self.note(meta('decisao',i,substitui_ids=['n_'+f'{j:032x}']),'08-Sistema/Decisoes/'+str(i)+'.md')
        self.assertFalse(audit.audit(self.root)['ok'])

    def test_module_cycle(self):
        for i,j in ((1,2),(2,1)):
            self.note(meta('modulo',i,dependencias_modulo=['n_'+f'{j:032x}']),'08-Sistema/Modulos/'+str(i)+'.md')
        self.assertFalse(audit.audit(self.root)['ok'])

    def test_inactive_project_excluded_from_focus_warning(self):
        self.note(meta('projeto',2,status='Pausado'),'03-Projetos/p.md')
        self.note(meta(status='Próxima ação',projeto_id='n_'+f'{2:032x}'))
        result=audit.audit(self.root);self.assertTrue(result['ok']);self.assertEqual(len(result['warnings']),1)

    def test_on_demand_active_needs_no_scheduler(self):
        self.note(meta('rotina',status='Ativa',gatilho='sob_demanda',criterio_aceite='Revisão registrada'),'06-Rotinas/r.md')
        self.assertTrue(audit.audit(self.root)['ok'])

    def test_scheduled_routine_needs_configuration(self):
        self.note(meta('rotina',status='Ativa',gatilho='agendado_app',criterio_aceite='Registro'),'06-Rotinas/r.md')
        self.assertFalse(audit.audit(self.root)['ok'])

    def test_duplicate_occurrence(self):
        for i in (1,2): self.note(meta('registro',i,chave_execucao='ocorrencia-ficticia'),'01-Diario/Execucoes/'+str(i)+'.md')
        self.assertFalse(audit.audit(self.root)['ok'])

    def test_bad_occurrence_type_reported(self): self.fails(meta(chave_execucao=['bad']))
    def test_unregistered_module_namespace(self): self.fails(meta(mod_estudos__curso_ref='curso'))

    def test_processed_capture_requires_destination(self):
        self.note(meta('captura',status='Processada'),'00-Inbox/c.md');self.assertFalse(audit.audit(self.root)['ok'])

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError): audit.strict_json('{"a":1,"a":2}')

    def test_secret_findings_do_not_echo_values(self):
        fake='sample_'+'x'*30
        self.put('07-Recursos/test.md','senha: "'+fake+'"\n')
        result=content.check(self.root);self.assertFalse(result['ok']);self.assertNotIn(fake,json.dumps(result))

    def test_credential_filename_reported(self):
        self.put('.env','dummy');self.assertFalse(content.check(self.root)['ok'])

    def test_path_rules(self):
        for name in ('../x','/x','a//b','a/./b','C:/x','a\\b','CON.txt','a.','a ','a?b','<x>','a|b','a\x01b'):
            with self.subTest(name=name), self.assertRaises(ValueError): audit.safe_relative(name)

    def test_symlink_rejected(self):
        p=self.root/'00-Inbox';p.mkdir()
        try: (p/'outside').symlink_to(self.base,target_is_directory=True)
        except OSError as exc:
            if getattr(exc,'winerror',None)==1314: self.skipTest('Windows sem privilegio para criar symlink')
            raise
        self.assertFalse(audit.audit(self.root)['ok'])

    def test_bundle_roundtrip_and_crlf(self):
        source=self.base/'spec.md';source.write_text(bundle_document({'a.txt':b'hello\n'}).replace('\n','\r\n'),encoding='utf-8',newline='')
        out=self.base/'extracted';result=bundle.extract(source,out)
        self.assertEqual((out/'a.txt').read_bytes(),b'hello\n');self.assertFalse(result['executed'])

    def test_bundle_hash_corruption_before_write(self):
        source=self.base/'spec.md';source.write_text(bundle_document({'a.txt':b'hello\n'}).replace('hello','changed'))
        out=self.base/'bad'
        with self.assertRaises(ValueError): bundle.extract(source,out)
        self.assertFalse(out.exists())

    def test_bundle_inventory_mismatch(self):
        text=bundle_document({'a.txt':b'hello\n'}).replace('"bytes": 6','"bytes": 99')
        with self.assertRaises(ValueError): bundle.parse_bundle(text)

    def test_bundle_path_escape(self):
        with self.assertRaises(ValueError): bundle.parse_bundle(bundle_document({'../x':b'x\n'}))

    def test_bundle_case_collision(self):
        with self.assertRaises(ValueError): bundle.parse_bundle(bundle_document({'a.txt':b'a\n','A.txt':b'b\n'}))

    def test_bundle_file_directory_collision(self):
        with self.assertRaises(ValueError): bundle.parse_bundle(bundle_document({'a':b'a\n','a/b':b'b\n'}))

    def test_extractor_preserves_existing_destination(self):
        source=self.base/'spec.md';source.write_text(bundle_document({'a.txt':b'a\n'}))
        with self.assertRaises(ValueError): bundle.extract(source,self.root)
        self.assertTrue((self.root/'AGENTS.md').exists())

    def test_snapshot_roundtrip_paused_and_other_bytes_identical(self):
        original=(self.root/'AGENTS.md').read_bytes();out=self.make_archive();dest=self.base/'restored'
        result=archive.restore(out,dest)
        self.assertEqual((dest/'AGENTS.md').read_bytes(),original)
        self.assertTrue(json.loads((dest/'08-Sistema/config.json').read_text())['global_pause'])
        self.assertFalse(result['external_schedules_changed']);self.assertTrue(audit.audit(dest)['ok'])

    def test_backup_refuses_destination_inside_source(self):
        with self.assertRaises(ValueError): archive.create(self.root,self.root/'backup.zip')

    def test_snapshot_omits_git_metadata(self):
        self.put('.git/config','not-exported');out=self.make_archive()
        self.assertNotIn('.git/config',archive.read_archive(out))

    def test_backup_rejects_credential_files(self):
        self.put('.env','dummy')
        with self.assertRaises(ValueError): archive.create(self.root,self.base/'bad.zip')

    def test_restore_preserves_existing_destination(self):
        out=self.make_archive()
        with self.assertRaises(ValueError): archive.restore(out,self.root)
        self.assertTrue((self.root/'AGENTS.md').exists())

    def test_restore_corruption_detected_before_destination(self):
        original=self.make_archive();bad=self.base/'corrupt.zip'
        with zipfile.ZipFile(original) as src,zipfile.ZipFile(bad,'w') as dst:
            for info in src.infolist():
                data=src.read(info.filename)
                if info.filename=='AGENTS.md': data=b'changed\n'
                dst.writestr(info.filename,data)
        dest=self.base/'bad-restore'
        with self.assertRaises(ValueError): archive.restore(bad,dest)
        self.assertFalse(dest.exists())

    def test_restore_rejects_zip_slip_entry(self):
        out=self.make_archive()
        with zipfile.ZipFile(out,'a') as z: z.writestr('../outside','bad')
        dest=self.base/'bad-restore'
        with self.assertRaises(ValueError): archive.restore(out,dest)
        self.assertFalse(dest.exists());self.assertFalse((self.base/'outside').exists())

    def test_restore_rejects_unmanifested_entry(self):
        out=self.make_archive()
        with zipfile.ZipFile(out,'a') as z: z.writestr('extra.txt','extra')
        with self.assertRaises(ValueError): archive.read_archive(out)

    def test_archive_size_limit(self):
        entries={'08-Sistema/config.json':b'{"schema_version":2,"global_pause":true}', 'too-big':b'x'*(archive.MAX_FILE+1)}
        with self.assertRaises(ValueError): archive.validate_inventory(entries)


if __name__=='__main__': unittest.main()
