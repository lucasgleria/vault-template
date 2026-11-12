# Adaptações aplicadas na implantação

O pacote foi extraído das nove entradas e todos os hashes/tamanhos de origem foram conferidos contra Implementation-euvih.md. O código original permanece integralmente nesse documento.

Na revisão aplicada ao euvih:

- O teste CRLF grava bytes sem a conversão adicional de newline do Windows.
- O teste de symlink informa skip quando o Windows nega o privilégio de criação; não conta como aprovado.
- Auditoria, extração e restauração rejeitam também junctions/reparse points do Windows. O teste adicional cria uma junction real e verifica a rejeição.
- O extrator aplicado importa a detecção de links de `audit_snapshot.py`; use o pacote completo. O extrator de entrada original continua no documento de origem.
- Na versão de template, `Indice.md` sem frontmatter é tratado como navegação derivada. Um índice com frontmatter continua sujeito aos contratos de nota. A triagem de conteúdo permanece ativa para ambos.

`manifesto.json` distingue versão e hashes de origem dos hashes/tamanhos aplicados. A biblioteca padrão e Python 3.11+ continuam suficientes. Nenhum auxiliar se tornou requisito de uso cotidiano.
