# Protocolo de operação do vault

Este procedimento implementa as seções 11–18 e 40 da especificação. AGENTS.md e a autorização atual governam sua aplicação. Os papéis de coordenar, executar, revisar e escrever podem ser exercidos pelo mesmo agente.

## Preparar

1. Identifique o pedido autenticado e o destino configurado. Durante o bootstrap, siga o onboarding para criar identidade e perfil. Em uso, confira o `vault_id` existente. Em Git, identifique também repositório e branch. Confira a autoridade pelo canal e pelas permissões efetivas.
2. Em Git, capture o HEAD `H`. Leia AGENTS, config, autonomia, perfil quando indicado, decisões e continuidade na revisão atual. Em outros destinos, capture as versões disponíveis dos arquivos e confira a raiz. Registre limites de consistência quando a ferramenta não oferecer leitura por revisão fixa.
3. Localize candidatos pela árvore e depois leia integralmente cada nota que será alterada. Uma busca vazia não prova ausência com paginação pendente ou índice atrasado. Recuse conteúdo truncado, symlinks e submódulos.
4. Expanda relações e dependências, confira origem e duplicatas. Consulte fontes atuais somente quando autorizadas e necessárias; registre cobertura, data e lacunas.
5. Prepare mudanças mínimas em UTF-8. Use os modelos de `../Templates/`, gere `n_` + 32 hex aleatórios apenas uma vez e preserve o ID em retries. Nada de exemplos fictícios como compromisso pessoal.
6. Valide campos, tipos, estados, relações, ausência de ciclos, fechamento, proveniência, dados mínimos, autorização, tamanho e política. A validação estrutural não autentica o consentimento.

## Aplicar por ferramentas reais

Para destino Git, prefira classe A, `createCommitOnBranch`, com `expectedHeadOid=H`, arquivos completos em base64 e um recibo em `08-Sistema/Operacoes/<operation_id>.json`. Os contratos GraphQL estão em `../../auxiliares/contracts/`. A credencial é resolvida pela conexão, fora das notas.

Para pasta ou serviço de arquivos, use as ferramentas efetivas de leitura e escrita. Compare versões ou bytes antes de editar e preserve mudanças alheias. Em lotes sequenciais, crie destinos antes dos links e grave `onboarding_status=configurado` por último, após conferir os outros arquivos. Se uma execução parar, registre o progresso parcial em continuidade e retome pela releitura. Um recibo pode usar o histórico do serviço ou a continuidade com caminhos e versões observadas. O modelo de recibo Git aplica-se às operações com base Git.

No template `novo`, identidade e perfil podem estar vazios. O primeiro lote persistido pode registrar progresso em `em_configuracao`. Gere os IDs uma vez e conclua apenas com perfil, destino, finalidade e coleções coerentes. Os valores vazios da configuração inicial são previstos no seu esquema. Notas de domínio aplicadas sempre usam IDs e campos completos.

O recibo contém `schema_version`, `operation_id`, referência mínima do pedido, `vault_id`, conexão observada, `base_commit`, autorização, motivo, IDs de entidades, digest, estado condicional, timestamp, fontes ausentes e ações externas pendentes. O campo opcional `domain_paths` registra a lista exata de caminhos cobertos.

Digest interoperável: construa o mapa `caminho → SHA-256 dos bytes posteriores`, usando `null` para exclusão. Ordene caminhos lexicograficamente, serialize JSON UTF-8 com `ensure_ascii=false`, sem espaços (`separators=(',', ':')`) e sem newline, e calcule SHA-256. Exclua o próprio recibo, todos os recibos técnicos, índices derivados e relatórios/checkpoints de evidência técnica. Declare as exclusões. Nunca inclua o hash do próprio commit no recibo que ele contém.

`clientMutationId` apenas correlaciona a chamada; a idempotência depende do recibo e da leitura do estado. Preserve `operation_id` e IDs em toda repetição da mesma tentativa lógica. Sem ID confiável de mensagem do canal, declare que a deduplicação entre sessões pode ser ambígua.

Classe B: a API REST de conteúdo usa o SHA anterior do arquivo. Essa proteção é por arquivo; limite a operações isoladas ou prepare uma branch e integração coerente. Não prometa lote atômico escrevendo notas uma a uma. Classe C: revalide a base atual antes da integração e declare limites do controle sobre a base.

O limite usual é 50 arquivos por operação e 262144 bytes por nota. Divida a implantação em lotes coerentes quando necessário; não relaxe limites silenciosamente. Não use force push, guard antigo, lock textual ou descarte de trabalho alheio para resolver concorrência.

## Confirmar e comunicar

Inspecione a resposta da ferramenta, inclusive erros GraphQL com HTTP 200. Retenha commit, revisão ou versões retornadas. Releia cada arquivo alterado no destino canônico e compare os bytes/valores esperados. Em Git, confira que o commit integra a branch configurada e se mudanças posteriores alteraram o resultado. Só então diga “registrei” ou “atualizei”.

Em proposta/PR: informe que aguarda integração. Em conflito: releia a base, preserve ambas as propostas e reconcilie por sentido. Em timeout: procure o recibo, digest, caminhos e histórico antes de repetir. Recibo com conteúdo diferente é colisão. Se não há prova suficiente, informe resultado desconhecido.

Falha de resposta depois de gravar exige recuperar o recibo e responder; não recriar entidades. Gravação parcial exige inventário por revisão e suspensão apenas dos leitores dependentes até reconciliação.

## Domínio e continuidade

Captura pode ser dispensada se o pedido já define tarefa clara. Triagem cria destinos e marca Processada no mesmo lote; não muda tipo mantendo identidade ambígua. Conclusão exige aceite, data real e evidência; cancelamento usa motivo/data próprios. Reabertura preserva fechamento anterior no histórico.

Para foco: selecione somente tarefas em Próxima ação/Em andamento, avulsas ou de projeto Ativo, com dependências concluídas, contexto disponível e sem decisão impeditiva. P1 não supera pausa. Até três prioridades é limite proposto, não obrigação de preencher vagas. Sem calendário atual, não afirme horários livres.

Registre no checkpoint apenas pedido minimizado, revisões, autorização, estado confirmado, lacunas e próxima ação. Não salve transcrição integral, respostas brutas ou raciocínio interno. Um novo agente relê o remoto e confere suas próprias capacidades.

## Fontes, efeitos e expansão

Consulte o [contrato de fontes](fontes-e-modulos.md). Antes de mensagem/evento/publicação, resolva autorização específica, alvo, conteúdo, precondição e recibo externo. Escrever no vault não comprova ação externa.

Módulo começa com necessidade demonstrada, reuso do núcleo, manifesto tipado, piloto autorizado, aceite e revisão. Nunca concede permissão. Pausa preserva legibilidade e exige tratar compromissos já assumidos. Migração precisa de inventário, mapa, revisão anterior preservada, validação e retorno; sem dados legados, não invente migração.

Referências da integração Git na especificação de origem, consultadas em 29/10/2026, estão em [commits](https://docs.github.com/en/graphql/reference/commits), [Git](https://docs.github.com/en/graphql/reference/git) e [conteúdo](https://docs.github.com/en/rest/repos/contents). Verifique as capacidades atuais da conexão antes de usar.
