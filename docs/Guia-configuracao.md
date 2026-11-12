> Guia de referência original. Para o estado aplicado, consulte [README](../README.md).

# Vault Adaptativo — guia de configuração e uso

**Versão:** 2.0.0 · **Data:** 29/10/2026  
**Compatível com:** `../Implementation-euvih.md`, versão 2.0.0 e contrato de dados 2.

O Vault Adaptativo organiza tarefas, projetos, responsabilidades, estudos, rotinas e conhecimento a partir de conversas com um agente de IA. **O GitHub privado guarda o estado canônico; o agente é a interface e o executor; o Obsidian é uma cópia local opcional do mesmo vault.**

Você utiliza a interface do agente que escolheu. Não precisa instalar Python, executar comandos, editar Markdown, abrir o GitHub ou manter um computador ligado durante o uso cotidiano em nuvem. A configuração inicial pode exigir autorizar uma conexão e selecionar o repositório correto.

Este guia acompanha a [especificação completa](../Implementation-euvih.md). Os dois documentos descrevem uma implantação futura. **Esta revisão não implementou o sistema, não modificou repositórios e não configurou contas ou serviços.**

## 1. Entenda os componentes

| Componente | Função |
|---|---|
| Especificação Markdown | Regras, contratos, modelos completos, implantação, recuperação e critérios de homologação. |
| Repositório privado no GitHub | Estrutura, notas, perfil, decisões, regras, modelos e histórico do vault aplicado. |
| Agente e integração | Interpretar pedidos, ler contexto, aplicar autorizações, persistir e verificar mudanças, responder. |
| Aplicativos externos | Fontes competentes de agenda, comunicação, documentos e dados especializados. |
| Obsidian opcional | Acesso a uma cópia local sincronizada, com os mesmos IDs e contratos. |
| Auxiliares opcionais | Auditoria e recuperação de exportações em ambiente técnico escolhido; não são o motor do sistema. |

GitHub não executa nem interpreta os agentes por guardar os arquivos. Uma rotina escrita descreve um procedimento; não cria um agendamento. Um recurso de memória da conversa não substitui gravação confirmada no repositório.

“Todos os dados do vault” não significa copiar senhas, caixas de e-mail, documentos externos completos ou bases operacionais dos aplicativos. O vault guarda o contexto mínimo necessário e referências para as fontes competentes.

## 2. Caminho principal de configuração

1. Escolher o agente em nuvem e uma integração suficiente com GitHub privado.
2. Selecionar o repositório e a branch canônica corretos, ou autorizar um destino novo quando necessário.
3. Verificar leitura, escrita, controle de versão e confirmação de gravação na integração real.
4. Materializar as regras, configuração, modelos e perfil mínimo pelos recursos do conector.
5. Fazer onboarding por conversa, definindo responsabilidades, fontes e autonomia.
6. Demonstrar uma jornada completa: pedido → contexto → alteração autorizada → verificação → resposta → retomada em outra sessão.
7. Conectar fontes, rotinas e módulos conforme a necessidade e a autorização.
8. Homologar recuperação e capacidades adicionais antes de prometer seu funcionamento.

Não há instalação local obrigatória nem necessidade de criar um servidor próprio em nuvem. Se a ferramenta não oferece escrita suficiente, ela pode servir para consulta; deve-se escolher uma integração adequada para operar todo o vault.

A configuração inicial é trabalho do agente implementador/responsável autorizado, usando as interfaces existentes. Ela não deve virar uma lista permanente de tarefas técnicas para o usuário.

## 3. Escolha o agente pelas capacidades

Zapia ou outro agente pode ser a interface desejada, mas o nome do produto não comprova integração privada, escrita, memória durável ou agendamento. Esta entrega não homologou um produto específico.

| Capacidade | Como comprovar na ferramenta escolhida |
|---|---|
| Identificar o alvo | Conferir usuário/canal, vault_id, repositório privado e branch. |
| Ler contexto atual | Abrir arquivo completo e identificar sua revisão, sem depender só de busca indexada. |
| Persistir | Criar/atualizar um registro reversível de teste no destino autorizado. |
| Evitar perda por concorrência | Demonstrar precondição de versão ou integração coerente de branch. |
| Confirmar | Reler os arquivos resultantes e verificar aplicação na branch canônica. |
| Consultar fontes | Testar cada calendário, arquivo ou aplicativo realmente conectado, com cobertura e data. |
| Executar agendado | Demonstrar disparo, ferramentas disponíveis na execução, persistência e entrega. |
| Pausar | Conferir tanto a nota/configuração quanto o disparador real. |
| Recuperar | Testar o procedimento escolhido e declarar o que está ou não coberto. |

Leitura sozinha permite análise, não organização persistente. Escrita de arquivo único não garante lote atômico de várias notas. As classes de integração da seção 14 da especificação definem as limitações.

Consultar documentação oficial atual e registrar a data, evidência, plano/versão quando expostos e limites. Um conector instalado não significa acesso validado; um teste de leitura não comprova envio de mensagens ou automação futura.

## 4. Autonomia sem aprovar cada commit

Defina por conversa o que o agente pode fazer sozinho. Exemplo de delegação a adaptar:

> Pode registrar e organizar os pedidos que eu fizer, relacionar registros existentes e atualizar os avanços que eu confirmar. Proponha mudanças maiores de objetivos ou projetos. Mensagens externas ficam como rascunhos até autorização correspondente.

O pedido explícito de criar uma tarefa autoriza essa criação no escopo. Ações internas reversíveis podem seguir delegação persistente, com recibo e possibilidade de correção. O agente não precisa pedir autorização técnica para cada commit.

Envio de mensagens, alteração de calendário, publicação, compartilhamento, contratação, operação financeira e ampliação de acesso continuam sujeitos à autorização específica ou delegação inequívoca. Criar módulo não concede permissões novas.

As políticas em arquivo orientam agentes conformes; não substituem controles técnicos da integração. Se for necessário impedir tecnicamente alterações de política por executores, verificar proteções e identidades disponíveis. Não apresentar um rótulo em Markdown como isolamento efetivo.

## 5. Onboarding progressivo

Comece com a responsabilidade que quer organizar e o resultado esperado. O agente aproveita as informações já fornecidas e pergunta somente o que afeta a próxima decisão.

- Papéis atuais e entregas reais.
- Fuso, quando houver data/horário que dependa dele.
- Fontes já utilizadas e quais deseja conectar.
- Capacidade, compromissos, descanso e restrições conhecidos.
- Autonomia e preferências de comunicação.
- Assuntos que não quer transformar em acompanhamento.

Desconhecidos permanecem desconhecidos. Uma captura simples não deve ser bloqueada porque o perfil está incompleto. O agente separa fatos confirmados, hipóteses e informações não verificadas.

O sistema não presume profissão, meta financeira, rotina de saúde ou prioridade universal. Interesse ocasional não vira obrigação; hobby não vira plano de renda; ideia não vira projeto Ativo sem intenção e capacidade.

## 6. Uso cotidiano pela conversa

| Necessidade | Pedido possível | Comportamento esperado |
|---|---|---|
| Capturar | “Guarde esta ideia para eu avaliar depois…” | Registrar sem inventar prazo ou prioridade. |
| Organizar entregas | “Comecei uma especialização; preciso organizar as entregas.” | Reaproveitar contexto, identificar resultados reais e perguntar só pelo necessário. |
| Definir foco | “O que merece minha atenção hoje?” | Filtrar estado de projetos, dependências e capacidade; até três prioridades iniciais. |
| Atualizar | “Avancei até aqui; falta…” | Registrar progresso sem concluir o que ainda falta. |
| Concluir | “Entreguei; a evidência é…” | Conferir aceite, origem e data, registrar fechamento adequado. |
| Aguardar | “Agora dependo desta resposta…” | Aguardando com dependência e acompanhamento pertinente. |
| Pausar | “Pause este projeto até eu decidir…” | Registrar condição de retorno e tirar tarefas do foco comum. |
| Estudar | “Ajude a organizar este conteúdo e minhas revisões.” | Separar aprendizado, recurso, tarefas e rotina quando úteis. |
| Revisar | “Faça a revisão semanal.” | Avaliar compromissos anteriores e propor próximos resultados realistas. |
| Corrigir | “Essa preferência mudou; agora…” | Atualizar a decisão pertinente e preservar o histórico. |
| Retomar | “Continue com o outro agente de onde ficou.” | Ler estado atual e checkpoint, sem depender da memória privada da conversa. |

P1 não significa automaticamente “fazer hoje”. Tarefa em Próxima ação de projeto Pausado ou Backlog não entra no foco só por seu status. Um aplicativo em uso pode ter seu desenvolvimento em Backlog.

A resposta do agente deve começar pelo resultado útil, mudanças realmente confirmadas, lacunas relevantes e primeira ação quando houver. IDs e commits podem permanecer nas evidências técnicas; não precisam aparecer em toda conversa.

## 7. O que significa “registrei”

O agente deve preparar a alteração, conferir autorização e versão, usar a escrita suportada e verificar o resultado. **Só depois da aplicação confirmada na branch canônica deve dizer “registrei”.**

| Estado real | Forma correta de comunicar |
|---|---|
| Apenas análise/conteúdo preparado | “Preparei a organização; ainda não foi gravada.” |
| Alteração em branch de proposta | “A alteração está preparada e aguarda integração.” |
| Persistência confirmada | “Registrei…” com síntese útil. |
| Falha conhecida antes da escrita | “Não foi possível registrar…” e próximo passo específico. |
| Timeout sem confirmação | “O resultado da gravação ainda não foi confirmado.” Consultar antes de repetir. |
| Parte de lote aplicada | Informar parcial e reconciliar antes de usar o estado dependente. |

Após falha de resposta, o agente consulta o recibo e o estado remoto para evitar duplicação. Não deve gerar novo identificador apenas para tentar de novo. Uma atualização interna do vault não comprova que uma mensagem foi enviada ou um evento foi criado.

## 8. Rotinas e agendamento são capacidades separadas

Uma rotina pode ser executada quando você pede durante a conversa, sem scheduler. Para execução futura, o agente/aplicativo precisa oferecer agendamento real com acesso às ferramentas necessárias naquele modo.

| Modo | O que está disponível |
|---|---|
| Sob demanda | O agente executa o procedimento durante a conversa e registra o resultado. |
| Agendamento nativo verificado | O aplicativo dispara a execução, com fontes, escrita, pausa e entrega homologadas. |
| Automação complementar escolhida | Um serviço em nuvem suporta o fluxo necessário, com autenticação e retorno testados. |
| Apenas lembrete | Convite para abrir conversa, se desejado; não é execução integral da rotina. |

Sem agendamento disponível, continue usando o procedimento pela conversa. Não é necessário instalar agendador local ou manter computador ligado para isso.

Pausa individual bloqueia a rotina ordinária; pedido explícito pode autorizar uma ocorrência excepcional sem reativar o conjunto. `global_pause` bloqueia automações não solicitadas, não impede capturas ou uma revisão pedida. Retomar não dispara automaticamente todo o histórico atrasado.

O disparador real também precisa ser pausado/conferido. Alterar uma nota não garante desligar uma tarefa externa que não lê o vault antes de agir. O agente deve informar esse limite e evitar novas ações fora da autorização.

## 9. Personalização e módulos

O núcleo é comum. Conforme o uso, o agente pode identificar responsabilidades e fluxos recorrentes, propor áreas, rotinas ou módulos e ativar dentro da autonomia concedida.

Cada módulo precisa demonstrar utilidade, reaproveitar tarefas/projetos/conhecimento, definir campos e fontes, testar um piloto e prever revisão, pausa e desativação. Não cria outro sistema paralelo. Novos acessos, custos e ações externas exigem autorização própria.

Exemplo: o início de um curso pode exigir somente projeto e tarefas. Se houver necessidade recorrente de acompanhar avaliações, revisões e materiais, um módulo de Estudos pode ajudar. Não é obrigatório ativá-lo na primeira menção.

Quando a necessidade acabar, os registros continuam legíveis. Pausar módulo não apaga compromissos já assumidos; eles precisam ser concluídos, transferidos ou cancelados explicitamente.

## 10. Obsidian e agentes locais opcionais

Se você quiser acesso local, utilize uma cópia sincronizada do mesmo repositório. Os IDs e regras permanecem os mesmos; o GitHub continua canônico.

Antes de enviar mudanças locais, preservar edições, obter o remoto, reconciliar diferenças, validar e confirmar a aplicação. Uma edição offline é pendente até a sincronização confirmada. Dois clones não compartilham um lock de diretório.

Escolha um mecanismo de sincronização e verifique seu comportamento; não presuma sincronização automática entre Obsidian e GitHub. Essa alternativa pode usar ferramentas gráficas ou agentes locais, sem impor comandos ao uso principal em nuvem.

Falha de sincronização local não elege o clone como canônico. A recuperação deve indicar explicitamente qual revisão vale, evitando duas bases independentes.

## 11. Migração de dados existentes

1. Preservar origem e revisão antes de converter.
2. Inventariar tipos, campos, estados, fontes, dados sensíveis e rotinas.
3. Separar regras gerais das preferências da pessoa.
4. Mapear IDs, relações, duplicatas, transformações e lacunas.
5. Preparar e validar em branch/destino autorizado.
6. Conferir contagens e amostras, sem inventar datas ou progresso.
7. Definir a virada para um único repositório/branch canônico.
8. Manter histórico necessário e plano de retorno.

A seção 31 da especificação contém o mapa 1.0.0 → 2.0.0. Não usar a antiga CLI local para operar o novo contrato sem adaptação. Aprovação textual de um script antigo não vira consentimento autenticado por migração.

## 12. Recuperação, privacidade e manutenção

Histórico de versões ajuda a recuperar arquivos, mas não substitui automaticamente uma cópia independente. Escolha um mecanismo compatível com as ferramentas existentes, sensibilidade e perda tolerável. Ele pode operar em nuvem; não exige máquina pessoal ligada.

Teste restauração em destino separado, confira notas/relações e mantenha automações pausadas antes de retomar. Rever efeitos externos após recuperação evita reenviar mensagens ou recriar eventos cujos recibos foram perdidos.

Credenciais permanecem fora do vault. Referências a calendário, e-mail e documentos não significam copiar seus conteúdos completos. Rótulo de sensibilidade não criptografa; apagar arquivo atual não elimina o histórico.

Manutenção pode ser solicitada por conversa: Inbox, projetos, conflitos, fontes antigas, módulos sem utilidade e permissões. Só prometer revisão automática se houver disparador homologado. Informar o que exige decisão, sem despejar logs na interface.

## 13. Como orientar um agente implementador

O pedido abaixo é para uso futuro e deve acompanhar permissões reais. Ler os documentos não autoriza modificar um vault existente por conta própria.

```text
Configure o Vault Adaptativo 2.0.0 conforme o README e a especificação completa.
Destino autorizado: [repositório privado e branch, ou autorização de destino novo].
Agente e integração escolhidos: [ferramentas existentes].
Fontes desejadas: [serviços; ou nenhuma por enquanto].
Autonomia e custos: [limites confirmados].
Dados existentes: [origens autorizadas; ou nenhum].

O uso principal deve ocorrer pela interface do agente em nuvem, sem instalação
local, Python, worker, servidor próprio ou manipulação cotidiana de arquivos.
GitHub é o armazenamento canônico; Obsidian e agentes locais são opcionais.
Verifique capacidades reais antes de prometer escrita ou agendamento.
Materialize regras/modelos pelo conector, faça onboarding por conversa e aplique
os protocolos de versão, confirmação, falha e continuidade.
Migre com evidência e retorno; homologue a jornada integral e a recuperação.
Ative só o que estiver autorizado e verificado. Entregue evidências e limitações.
```

Para solicitar somente documentação, mantenha esse limite explícito. Os scripts opcionais não precisam ser extraídos para preparar ou operar o sistema principal.

## 14. Roteiro de leitura da especificação

| Necessidade | Seções |
|---|---|
| Arquitetura, capacidade e fontes | 1–6 |
| Dados, estados e personalização | 7–10 |
| Leitura, escrita, conflitos e autorização | 11–18 |
| Captura, tarefas, projetos, foco e estudos | 19–23 |
| Rotinas, agendamento e módulos | 24–28 |
| Cópia local, recuperação, migração e implantação | 29–32 |
| Jornadas, homologação e operação | 33–36 |
| Contratos e modelos completos | 37–40 |
| Revisão dos scripts e pacote opcional | 41–42 |
| Verificação, mudanças e referências | 43–45 |

## 15. Estado desta entrega

Foram reescritos a especificação e este guia, com arquitetura consistente, contratos, modelos, fluxos e critérios de homologação. Os auxiliares opcionais têm manifesto e hashes novos; o resultado dos testes realizados nesta revisão está na seção 43 da especificação.

Não foram testados acesso autenticado a um vault real, conector de um produto específico, escrita remota, agendamento, permissões de conta, notificações ou recuperação em serviço externo. Esses resultados dependem das ferramentas escolhidas e devem ser demonstrados na implantação.

O critério central é concreto: uma pessoa consegue pedir ajuda, ter alterações autorizadas persistidas e verificadas e retomar com outro agente pela própria interface em nuvem, sem instalar ferramentas locais ou manipular arquivos no cotidiano.
