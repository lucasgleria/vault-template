---
id: "n_c1acb4c0dbfc4ce8b2961547e6a3cef8"
schema_version: 2
tipo: "rotina"
titulo: "Revisão de projeto"
status: "Rascunho"
criado: "2026-10-29T23:53:05+00:00"
atualizado: "2026-10-29T23:53:05+00:00"
origem: "conversa-autenticada"
origem_ref: "sessao:implantacao-euvih-2026-10-29"
confianca: "confirmado"
sensibilidade: "pessoal"
area_id: null
projeto_id: null
objetivo_ids: []
fontes: []
modulos: []
aliases: []
tags: []
evidencias: []
gatilho: "sob_demanda"
timezone: null
agenda_ref: null
disparador_ref: null
agendamento_status: "nao_solicitado"
janela_min: null
politica_atraso: "ignorar"
max_tentativas: 1
criterio_aceite: "Resultado, risco, próxima ação e decisão necessária registrados."
canal_entrega_ref: null
versao_procedimento: "1.0.0"
---

# Revisão de projeto

## Objetivo, entradas, procedimento e aceite
Ler resultado, aceite, última decisão, tarefas, artefatos e dependências. Identificar avanço e risco concretos; propor uma próxima ação e uma decisão quando necessária. Conferir se o projeto ainda merece capacidade. Não abrir novo projeto para cada dificuldade.

## Pré-condições e execução por conversa
Este procedimento está em Rascunho. Um pedido direto pode autorizar a execução pontual, sem ativação recorrente.
Ler AGENTS.md, config, autonomia, perfil e decisões na revisão atual. Conferir fontes e cobertura.
Não existe agenda nem disparador externo. global_pause continua true e permite pedidos explícitos.
Não executar check-ins sem propósito e consentimento correspondentes.

## Identidade da ocorrência
Usar vault_id + rotina_id + período/escopo do pedido; preservar a chave em repetição.
Conferir recibo e ocorrência existentes antes de reservar. Reservar com precondição de branch se houver execução concorrente.
Uma atualização da mesma revisão/período modifica a ocorrência existente. Reexecução deliberada exige motivo e vínculo.

## Registro e entrega
Criar Registro em 01-Diario/Execucoes/ com rotina_id, chave_execucao, tentativa e estados separados.
Para revisões, usar 01-Diario/Revisoes/ e período real; o modelo semanal está em 08-Sistema/Templates/.
Fontes ausentes produzem resultado parcial quando limitam a cobertura. Nenhuma fonte vazia por falha vira zero.
Gravar resultado e recibo coerentes; confirmar bytes e presença canônica antes de responder.
Entrega pela conversa não autoriza mensagem proativa. Não preencher entregue antes do retorno efetivo.

## Pausa, falhas e retomada
Pausada bloqueia execução ordinária; exceção requer pedido explícito. Desativada exige decisão nova.
Pausar e verificar também o disparador real, caso um dia exista. Nunca recuperar todos os slots atrasados automaticamente.
Timeout: consultar recibo/ocorrência antes de repetir. Cota: checkpoint; sem fallback pago automático.
Uma tentativa cancelada não pode finalizar sobre tentativa posterior.
