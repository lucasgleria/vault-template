#!/usr/bin/env python3
"""ZIP opcional de exportacao estavel; restore novo e pausado; sem rede/criptografia."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import stat
import zipfile
from audit_snapshot import regular_files, safe_relative, strict_json, is_link

MAX_FILE = 2_000_000
MAX_TOTAL = 50_000_000
MAX_FILES = 10000
MANIFEST_NAME = 'BACKUP-MANIFEST.json'


def digest(data): return hashlib.sha256(data).hexdigest()


def validate_inventory(entries):
    if not entries or len(entries)>MAX_FILES: raise ValueError('inventario vazio ou grande')
    names = set()
    for name,data in entries.items():
        safe_relative(name)
        if name.casefold() in names or len(data)>MAX_FILE: raise ValueError('colisao ou arquivo grande')
        names.add(name.casefold())
    if sum(map(len,entries.values()))>MAX_TOTAL: raise ValueError('snapshot grande')
    for name in entries:
        parts=name.split('/')
        if any('/'.join(parts[:i]).casefold() in names for i in range(1,len(parts))): raise ValueError('colisao de caminho')
    config = strict_json(entries.get('08-Sistema/config.json',b'null').decode('utf-8'))
    if not isinstance(config,dict) or config.get('schema_version') != 2 or type(config.get('global_pause')) is not bool:
        raise ValueError('config schema 2 e pausa explicita obrigatorios')


def create(snapshot, archive, revision=None):
    source = Path(snapshot)
    if is_link(source): raise ValueError('origem simbolica')
    source = source.resolve(); out = Path(archive).absolute()
    if out.exists() or is_link(out): raise ValueError('arquivo de destino ja existe')
    if not out.parent.is_dir() or any(is_link(p) for p in (out.parent,*out.parent.parents)): raise ValueError('pai ausente ou simbolico')
    if out.resolve()==source or source in out.resolve().parents: raise ValueError('destino deve ficar fora da origem')
    entries={}
    for path in regular_files(source):
        rel=path.relative_to(source).as_posix()
        if rel==MANIFEST_NAME: raise ValueError('nome reservado')
        if path.name.startswith('.env') or path.suffix.lower() in ('.key','.pem','.pfx'): raise ValueError('arquivo de credencial recusado')
        if path.stat().st_size>MAX_FILE: raise ValueError('arquivo grande')
        entries[rel]=path.read_bytes()
    validate_inventory(entries)
    manifest={'format':2,'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),
              'source_revision':revision,'files':{n:{'bytes':len(b),'sha256':digest(b)} for n,b in sorted(entries.items())}}
    created=False
    try:
        with out.open('xb') as target:
            created=True
            with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
                for name,data in sorted(entries.items()): z.writestr(name,data)
                z.writestr(MANIFEST_NAME,json.dumps(manifest,ensure_ascii=False,sort_keys=True)+'\n')
        read_archive(out)
    except Exception:
        if created and out.exists(): out.unlink()
        raise
    return {'archive':str(out),'files':len(entries),'sha256':digest(out.read_bytes()),'encrypted':False,'source_revision':revision}


def read_archive(archive):
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist(); names=[i.filename for i in infos]
        if len(names)!=len(set(names)) or len(names)>MAX_FILES+1: raise ValueError('entradas repetidas/excessivas')
        if MANIFEST_NAME not in names: raise ValueError('manifesto ausente')
        if sum(i.file_size for i in infos)>MAX_TOTAL+MAX_FILE: raise ValueError('arquivo excede limite')
        for info in infos:
            safe_relative(info.filename)
            if info.file_size>MAX_FILE or info.is_dir() or stat.S_ISLNK(info.external_attr>>16): raise ValueError('entrada insegura')
        manifest=strict_json(z.read(MANIFEST_NAME).decode('utf-8'))
        if not isinstance(manifest,dict) or manifest.get('format')!=2 or not isinstance(manifest.get('files'),dict): raise ValueError('manifesto invalido')
        if set(names)!=(set(manifest['files'])|{MANIFEST_NAME}): raise ValueError('inventario divergente')
        entries={}
        for name,entry in manifest['files'].items():
            data=z.read(name)
            if not isinstance(entry,dict) or entry.get('bytes')!=len(data) or entry.get('sha256')!=digest(data): raise ValueError('integridade invalida')
            entries[name]=data
        validate_inventory(entries)
        return entries


def restore(archive, destination):
    entries=read_archive(archive)  # Verificar todo o conteudo antes de criar destino.
    dest=Path(destination).absolute()
    if dest.exists() or is_link(dest): raise ValueError('restaure em destino inexistente')
    if not dest.parent.is_dir() or any(is_link(p) for p in (dest.parent,*dest.parent.parents)): raise ValueError('pai ausente ou simbolico')
    config=strict_json(entries['08-Sistema/config.json'].decode('utf-8')); config['global_pause']=True
    entries['08-Sistema/config.json']=(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    dest.mkdir()
    try:
        for name,data in entries.items():
            path=dest.joinpath(*safe_relative(name)); path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as f: f.write(data)
    except Exception:
        shutil.rmtree(dest); raise
    return {'restored':str(dest),'files':len(entries),'paused_in_config':True,
            'modified_by_restore':['08-Sistema/config.json'],'external_schedules_changed':False}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('create'); c.add_argument('snapshot'); c.add_argument('archive'); c.add_argument('--revision')
    r=sub.add_parser('restore'); r.add_argument('archive'); r.add_argument('destination')
    a=p.parse_args()
    try:
        result=create(a.snapshot,a.archive,a.revision) if a.cmd=='create' else restore(a.archive,a.destination)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,OSError,UnicodeError,zipfile.BadZipFile) as exc: p.exit(2,str(exc)+'\n')
