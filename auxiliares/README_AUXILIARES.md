# Auxiliares opcionais — Vault Adaptativo 2.0.0

O uso principal acontece pela interface de um agente em nuvem com integração
suficiente ao GitHub privado. Estes arquivos não são uma instalação do sistema.
Não são necessários no computador do usuário e não conectam contas.

Um técnico ou ambiente temporário de agente, se escolhido, pode usar Python 3.11+
para conferir uma exportação estável e já autorizada. Nenhum script faz rede,
executa IA, grava no repositório remoto ou instala um serviço.

- scripts/audit_snapshot.py: lê notas schema 2, valida o subconjunto documentado
  de identidade, campos, relações e fechamento. Não verifica verdade ou autorização.
- scripts/check_content.py: heurística redigida de possíveis segredos. Não certifica
  ausência de dados sensíveis e não exibe os valores encontrados.
- scripts/snapshot_archive.py: cria ZIP verificado de uma cópia estável e restaura
  em diretório novo, com global_pause=true. ZIP não é criptografia; não inclui Git,
  Obsidian, ambiente virtual ou credenciais. Não controla agendadores externos.
- scripts/extract_bundle.py: confere manifesto/hashes antes de extrair; não executa
  os arquivos. Hashes não autenticam o autor do documento.
- contracts/*.graphql: exemplos de contrato para conector; não são executados aqui.
- tests/test_auxiliaries.py: testes offline com dados fictícios e temporários.

Comandos opcionais a partir desta pasta, em ambiente técnico já escolhido:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/audit_snapshot.py /copia-estavel-do-vault
python3 scripts/check_content.py /copia-estavel-do-vault
python3 scripts/snapshot_archive.py create /copia-estavel-do-vault /destino-protegido/snapshot.zip --revision COMMIT_OBSERVADO
python3 scripts/snapshot_archive.py restore /destino-protegido/snapshot.zip /destino-novo
```

Substitua caminhos por destinos reais. Uma cópia deve ser de uma revisão conhecida,
sem alterações simultâneas. Os scripts não garantem snapshot de arquivos em edição.
No Windows, pode-se usar o executável Python existente equivalente; sua instalação
não é etapa do caminho principal. Não usar extração/restauração em diretórios
compartilhados com processos não confiáveis: não são uma sandbox contra corridas
maliciosas do sistema de arquivos.
