# Vault adaptativo

Abra este projeto em um agente com acesso aos arquivos. As instruções da raiz orientam o agente a iniciar a configuração na primeira interação disponível, perguntando o que você quer organizar e qual resultado espera. Responda pela conversa. O agente usa suas respostas para montar o vault dentro desta estrutura.

A entrada principal fica em [AGENTS.md](AGENTS.md). O projeto também inclui arquivos de entrada para Claude Code, Gemini CLI e GitHub Copilot. Cada um aponta para o mesmo contrato e para a mesma configuração. Codex e Cursor reconhecem `AGENTS.md`. Os mecanismos de carregamento são descritos nas documentações oficiais de [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Cursor](https://cursor.com/docs/rules), [Claude Code](https://code.claude.com/docs/en/memory), [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/) e [Copilot](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions).

O carregamento depende do aplicativo e das instruções de projeto habilitadas. A entrevista acontece quando o aplicativo dá ao agente uma interação. Em outro chat com acesso ao projeto, uma saudação ou o pedido “configure este vault comigo” pode iniciar a mesma entrada. Para gravar a estrutura diretamente, o agente precisa de escrita no destino. Com leitura, ele prepara os arquivos para aplicação posterior.

## Como a configuração funciona

O agente faz uma pergunta por vez e aproveita informações já dadas. Descobre a finalidade, o público de uso, a maneira de guardar e encontrar o conteúdo e apenas as preferências necessárias. A partir das escolhas, preenche o perfil, a configuração, o mapa e a página inicial. Pode atender estudos, projetos, trabalho, escrita, pesquisa, referências ou outras finalidades usando os tipos comuns e os módulos previstos.

O estado começa em `novo`. Durante a conversa pode passar a `em_configuracao`, com decisões salvas para retomada. Só chega a `configurado` depois da aplicação e da conferência dos arquivos. Uma sessão posterior lê esse estado para continuar o uso ou a configuração em andamento.

## Estrutura existente

| Local | Uso quando necessário |
| --- | --- |
| `00-Inbox/` | Conteúdo a triar. |
| `01-Diario/` | Registros, revisões e ocorrências. |
| `02-Tarefas/` | Ações verificáveis. |
| `03-Projetos/` | Resultados com fim. |
| `04-Areas/` | Responsabilidades contínuas. |
| `05-Conhecimento/` | Informação reutilizável. |
| `06-Rotinas/` | Procedimentos repetíveis. |
| `07-Recursos/` | Materiais e referências de apoio. |
| `08-Sistema/` | Configuração, perfil, decisões, modelos e contratos. |

O agente usa apenas os locais necessários e escolhe suas subdivisões conforme a finalidade. As pastas de conteúdo aparecem com seus primeiros registros ou índices. Os treze modelos existentes e os sete procedimentos de rotina são a base reutilizável. Os exemplos de agenda e Estudos podem apoiar uma escolha posterior.

Use [Início](Inicio.md) para navegar, [onboarding](08-Sistema/Continuidade/onboarding.md) para entender a entrevista e [estrutura](08-Sistema/Continuidade/estrutura.md) para consultar a organização escolhida. As instruções de [operação](08-Sistema/Agentes/protocolo.md) preservam identidade, controle de versão e confirmação da gravação.

A configuração aceita uma pasta, um repositório ou um serviço de arquivos como destino canônico. Em Git, a branch escolhida define onde confirmar as alterações. O uso em nuvem depende das ferramentas do agente. Obsidian e cópias locais podem ser usados quando fizerem sentido.

## Origem e verificações

Este template reaproveita o euvih. A [especificação 2.0.0](Implementation-euvih.md) e o [guia original](docs/Guia-configuracao.md) documentam a origem. As regras operacionais atuais estão em `AGENTS.md` e `08-Sistema/`. A validação estrutural atual está descrita em [contratos](08-Sistema/Esquemas/README.md).
