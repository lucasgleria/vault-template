# Configuração inicial pela conversa

## Iniciar e retomar

Leia `AGENTS.md`, a configuração, a autonomia e `atual.md` antes da primeira resposta da sessão. Em `novo`, aproveite o pedido atual e inicie pela finalidade que estiver em aberto.

> O que você quer organizar neste vault e o que gostaria de conseguir com ele?

Faça uma pergunta curta por vez. Adapte a próxima pergunta à resposta anterior. Em `em_configuracao`, retome da pendência registrada. Em `configurado`, atenda ao uso normal e reconfigure apenas o que a pessoa solicitar. No estado legado `em_descoberta`, aproveite o perfil existente e as decisões vigentes.

Um pedido específico de manutenção, análise ou implementação segue seu próprio objetivo. Uma captura pedida pode ser atendida durante a descoberta. As informações necessárias para essa ação podem orientar a próxima pergunta.

## Descobrir as escolhas necessárias

| Escolha | Como descobrir |
| --- | --- |
| Finalidade | O que a pessoa quer guardar, acompanhar, produzir ou encontrar, e qual resultado espera. |
| Público e limites | Quem vai usar o vault, quais informações podem ficar no destino e quem decide sobre conteúdo compartilhado. Aproveite o que já estiver claro no pedido. |
| Organização | Pergunte como costuma procurar as informações. Proponha uma divisão pequena ligada ao caso e esclareça as alternativas que realmente mudam o uso. |
| Nome e comunicação | Aproveite nome e idioma informados. Proponha um nome simples quando a escolha for delegada. Pergunte por fuso somente quando datas e horários dependerem dele. |
| Fontes e fluxos | Pergunte por materiais existentes, tarefas, revisões ou rotinas quando a finalidade pedir. Um interesse mencionado só vira acompanhamento se a pessoa escolher isso. |

Use a raiz aberta como local de trabalho do bootstrap. Confira acesso, escopo e visibilidade antes de guardar informações. Se o usuário escolher a própria pasta como canônica, `destino` terá `tipo: "pasta"` e uma referência suficiente para reencontrá-la, que pode ser `.` em um projeto aberto. Para Git canônico, confirme o repositório e a branch, preencha também `repositorio` e verifique a integração. Um remoto herdado de uma cópia do template precisa ser conferido com o destino escolhido. Para armazenamento de arquivos conectado, use `tipo: "servico"` e o identificador da raiz. Em pasta ou serviço, mantenha `repositorio: null`. Escolhas ambíguas de destino exigem esclarecimento antes da escrita dependente.

Quando houver finalidade, público, destino e uma organização escolhida ou delegada, apresente brevemente o que será montado e aplique as escolhas internas. As respostas sobre a configuração e a delegação de escolhas reversíveis dão o escopo dessa montagem. Uma pergunta aberta ainda exige resposta. Migração de dados existentes, publicação, mensagens, agendamentos, novos acessos e gastos dependem de autorização correspondente.

## Configurar dentro desta estrutura

1. Reaproveite os diretórios `00-Inbox/` a `08-Sistema/` e os modelos em `08-Sistema/Templates/`. Escolha apenas os tipos e locais úteis. Organize assuntos, coleções e contextos com subpastas, relações e títulos. Os campos especializados seguem o contrato de módulos existente.
2. Gere uma vez `vault_id` com `v_` e 32 hexadecimais minúsculos. Preserve IDs nas retomadas. Preencha `proprietario_ref` com uma referência mínima ao responsável no canal autenticado, sem inferir identidade por nome de conta. Crie o perfil com `Templates/perfil.md`, usando `n_` e 32 hexadecimais, e salve em `08-Sistema/Perfis/<id>.md`. Aproveite o perfil já indicado quando houver um.
3. Preencha nome, finalidade, destino e idioma em `config.json`. Mantenha desconhecidos pertinentes como `null`. Registre em `estrutura` as chaves de coleção e seus diretórios, por exemplo `referencias` apontando para uma subdivisão de `05-Conhecimento/`. Use caminhos relativos portáveis, sem `..`, dentro dos diretórios de conteúdo existentes. Uma estrutura configurada precisa de ao menos uma coleção.
4. Atualize `estrutura.md` com o propósito, o público, o que entra em cada coleção, os tipos de nota e os caminhos para recuperar conteúdo. Atualize `Inicio.md` com os links úteis. Use `Indice.md` como página derivada de navegação, em Markdown simples, quando precisar representar uma coleção ainda sem conteúdo em Git. Índices com frontmatter são tratados como notas e seguem o contrato completo. Leia índices existentes antes de alterar.
5. Registre no perfil os fatos e preferências confirmados. Use decisões quando a escolha mudar regras ou direção. Atualize `atual.md` com as escolhas, a próxima pergunta e as referências de aplicação. Na autonomia, preencha responsável, data real e origem da configuração. Preserve as regras de autorização e registre delegações adicionais apenas quando expressas.
6. Crie notas de domínio apenas com conteúdo real que a pessoa pediu para guardar. As rotinas já fornecidas permanecem procedimentos em rascunho e podem ser usadas sob demanda. Use os módulos conforme a necessidade e a autorização demonstradas.
7. Siga `08-Sistema/Agentes/protocolo.md` para aplicar e verificar. Durante progresso parcial persistido, use `em_configuracao`. Em lote atômico, `configurado` pode integrar o lote completo. Em gravação sequencial, grave essa marca por último, depois de conferir perfil, coleções, índices e conteúdo. Releia a marca e os arquivos finais no destino canônico. Resuma o que a pessoa já pode fazer e indique `Inicio.md`.

## Continuidade e limites de ferramenta

Salve decisões mínimas e a próxima pergunta quando a escrita estiver disponível e o destino identificado. Na retomada, confira o estado atual para evitar repetição de perguntas e duplicação de entidades. Em falta de escrita, continue a entrevista e entregue a proposta com caminhos e conteúdos dos arquivos. Indique a aplicação pendente e as verificações necessárias para concluir.

Cada agente mede suas ferramentas nesta sessão. A configuração pode funcionar pela pasta aberta sem dependência de instalação, scripts ou um agente específico. A execução de uma entrevista em um aplicativo precisa ser observada antes de atribuir homologação àquela integração.
