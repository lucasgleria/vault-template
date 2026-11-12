# Contratos de dados

Notas são Markdown UTF-8 com frontmatter restrito: uma chave por linha, valor JSON, escalares/null/listas simples; sem objetos, âncoras, tags ou chaves repetidas. ID é `n_` + 32 hex aleatórios, estável e único.

`nota.schema.json` declara campos, tipos, estados e condições estruturais. Os modelos completos em `../Templates/` são material de preenchimento, não entidades reais. Placeholders só podem permanecer nos modelos, nunca em arquivo ativo que dependa deles.

`Indice.md` em uma coleção pode ser uma página derivada de navegação em Markdown simples. Os validadores preservam a triagem de seu conteúdo e o excluem da contagem de entidades. Quando tiver frontmatter, o índice segue o contrato de nota e mantém sua identidade.

Relações tipadas, ciclos, coerência de fechamento, projeto elegível e autoridade de evidência também exigem validação semântica. O auditor em `../../auxiliares/scripts/audit_snapshot.py` cobre o subconjunto declarado na especificação. O verificador em `../../ferramentas/validar.py` acrescenta contratos locais e projeção de elegibilidade; nenhum deles prova verdade factual, autorização autenticada ou disponibilidade de produto.

`operacao.schema.json`, `config.schema.json` e `modulo.schema.json` descrevem os respectivos documentos. O protocolo de serialização e exclusões do digest está em `../Agentes/protocolo.md`.

A configuração 2.1 aceita `novo` e `em_configuracao` com identidade e perfil ainda vazios. Em `configurado`, exige identidade, responsável, perfil, nome, finalidade, destino e uma coleção existente. `destino` distingue pasta, Git e serviço de arquivos. Os caminhos de `estrutura` usam os diretórios de conteúdo originais. O estado legado `em_descoberta` continua compatível com a configuração Git anterior. A existência do perfil e das coleções e a coerência entre destino Git e repositório são verificadas semanticamente por `validar.py`.

Uso técnico opcional, sem instalação de dependências:

```text
python -X utf8 ferramentas/validar.py .
python -X utf8 -m unittest discover -s tests -v
python -X utf8 -m unittest discover -s auxiliares/tests -v
```

O agente pode realizar as mesmas verificações com suas ferramentas nativas. Esses comandos não são o motor da organização nem requisito do uso cotidiano.
