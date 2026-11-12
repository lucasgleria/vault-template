#!/usr/bin/env python3
"""Extrai auxiliares opcionais verificados; nao instala nem executa arquivos."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
from audit_snapshot import is_link

BLOCK = re.compile(
 r'^<!-- VAULT-FILE path=([A-Za-z0-9_./-]+) sha256=([0-9a-f]{64}) -->\n'
 r'^````[A-Za-z0-9_-]*\n(.*?)^````\n<!-- END-VAULT-FILE -->$', re.M | re.S)
MANIFEST = re.compile(
 r'^<!-- VAULT-MANIFEST version=2.0.0 -->\n^````json\n(.*?)^````\n'
 r'<!-- END-VAULT-MANIFEST -->$', re.M | re.S)


def safe_name(name):
    if not name or name.startswith('/') or '\\' in name or ':' in name: raise ValueError('caminho invalido')
    if any(ord(c)<32 or c in '<>"|?*' for c in name): raise ValueError('caractere de caminho invalido')
    parts = name.split('/')
    reserved = {'CON','PRN','AUX','NUL'} | {f'{p}{i}' for p in ('COM','LPT') for i in range(1,10)}
    if any(p in ('','.','..') or p.endswith((' ','.')) or p.split('.')[0].upper() in reserved for p in parts):
        raise ValueError('caminho nao portavel')
    return parts


def parse_bundle(text):
    text = text.replace('\r\n','\n')
    manifests = MANIFEST.findall(text)
    if len(manifests) != 1: raise ValueError('manifesto unico obrigatorio')
    manifest = json.loads(manifests[0])
    if manifest.get('version') != '2.0.0' or not isinstance(manifest.get('files'),dict): raise ValueError('manifesto invalido')
    blocks = BLOCK.findall(text)
    if len(blocks) != len(re.findall(r'^<!-- VAULT-FILE path=', text, re.M)): raise ValueError('bloco incompleto')
    files, names = {}, set()
    for name, expected, body in blocks:
        safe_name(name)
        if name.casefold() in names: raise ValueError('caminho duplicado ou colisao de caixa')
        names.add(name.casefold())
        data = body.encode('utf-8')
        if len(data) > 2_000_000 or hashlib.sha256(data).hexdigest() != expected: raise ValueError('hash/tamanho invalido')
        entry = manifest['files'].get(name)
        if not isinstance(entry,dict) or entry.get('sha256') != expected or entry.get('bytes') != len(data): raise ValueError('divergencia do manifesto')
        files[name] = data
    if not files or set(files) != set(manifest['files']): raise ValueError('inventario incompleto')
    if len(files)>100 or sum(map(len,files.values()))>20_000_000: raise ValueError('pacote excede limite')
    for name in files:
        parts = name.split('/')
        if any('/'.join(parts[:i]).casefold() in names for i in range(1,len(parts))): raise ValueError('colisao arquivo/diretorio')
    return files


def extract(document, destination):
    files = parse_bundle(Path(document).read_text(encoding='utf-8'))
    dest = Path(destination).absolute()
    if dest.exists() or is_link(dest): raise ValueError('destino deve ser inexistente')
    if not dest.parent.is_dir() or any(is_link(p) for p in (dest.parent,*dest.parent.parents)):
        raise ValueError('pai ausente ou simbolico')
    dest.mkdir()
    try:
        for name,data in files.items():
            path = dest.joinpath(*safe_name(name)); path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as f: f.write(data)
    except Exception:
        shutil.rmtree(dest); raise
    return {'files':len(files),'destination':str(dest),'executed':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('document'); p.add_argument('destination')
    args = p.parse_args()
    try: print(json.dumps(extract(args.document,args.destination),ensure_ascii=False))
    except (ValueError,OSError,UnicodeError) as exc: p.exit(2, str(exc)+'\n')
