#!/usr/bin/env python3
"""Triagem opcional, sem escrita e sem mostrar valores; heuristica incompleta."""
import argparse
import json
import re
from pathlib import Path
from audit_snapshot import regular_files

PATTERNS = {
 'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'bearer_literal': re.compile(r'(?i)authorization\s*[:=]\s*[\"\x27]?bearer\s+[A-Za-z0-9._-]{20,}'),
 'credential_assignment': re.compile(r'(?i)(?:api_key|access_token|password|senha)\s*[:=]\s*[\"\x27][^\"\x27\n]{12,}[\"\x27]'),
 'connection_credentials': re.compile(r'(?i)postgres(?:ql)?://[^\s/:]+:[^\s@]+@')}


def check(root):
    root = Path(root); findings = []
    try: files = regular_files(root)
    except (ValueError, OSError):
        return {'ok':False,'findings':[{'path':'.','rule':'invalid_or_unsafe_snapshot'}]}
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.name.startswith('.env') or path.suffix.lower() in ('.key','.pem','.pfx'):
            findings.append({'path':rel,'rule':'forbidden_filename'}); continue
        if path.suffix.lower() not in ('.md','.json','.txt','.yaml','.yml','.graphql'): continue
        if path.stat().st_size > 2_000_000:
            findings.append({'path':rel,'rule':'not_scanned_size'}); continue
        try: content = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            findings.append({'path':rel,'rule':'not_scanned_encoding_or_access'}); continue
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(content):
                findings.append({'path':rel,'rule':name,'line':content.count('\n',0,match.start())+1})
    return {'ok':not findings,'findings':findings,
            'limitation':'heuristica; nao certifica ausencia de segredos ou dados pessoais'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('snapshot')
    result = check(p.parse_args().snapshot)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
