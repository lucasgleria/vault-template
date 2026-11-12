---
id: "__N_ID_32_HEX__"
schema_version: 2
tipo: "rotina"
titulo: "__TITULO_DESCRITIVO__"
status: "Rascunho"
criado: "__TIMESTAMP_COM_OFFSET__"
atualizado: "__TIMESTAMP_COM_OFFSET__"
origem: "__ORIGEM_LOGICA__"
origem_ref: null
confianca: "nao_verificado"
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
criterio_aceite: "__RESULTADO_E_CONFERENCIA__"
canal_entrega_ref: null
versao_procedimento: "1.0.0"
---

# Procedimento de rotina

## Objetivo
Decisão ou resultado que deve facilitar, sem presumir agendamento.

## Entradas e fontes
Dados mínimos, autoridade, cobertura e frescor necessários.

## Pré-condições
Estado, pedido/delegação, capacidade, pausa e ocorrência não duplicada.
Rotina sob demanda não exige agenda; rotina pausada só admite exceção explícita.

## Procedimento
1. Ler regras e fontes pertinentes.
2. Reconciliar decisões, estado e capacidade.
3. Produzir resultado dentro do escopo.
4. Validar conteúdo, evidências e lacunas.
5. Persistir registro, confirmar e responder/entregar pelo canal permitido.

## Saída e aceite
Formato, tamanho, resultado esperado e evidência de persistência.

## Disparo e pausa
Sob demanda, aplicativo agendado ou automação escolhida. ID/estado remoto separado.
Pausa da nota não substitui conferir o disparador. Não recuperar slots antigos sozinho.

## Falhas e supressão
Fonte ausente, cota, resultado incerto, tentativas e notificações sem resposta.
