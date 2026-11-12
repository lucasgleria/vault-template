# Contratos de fontes e módulos

## Consulta de fonte

Uma consulta informa request_id, source_id, operação realmente suportada, parâmetros, propósito e read_only. O resultado informa observed_at, status, freshness, items, next_cursor, complete, coverage e warnings. Estados permitidos: ok, partial, unavailable, unauthorized, rate_limited, invalid_response. Frescor: live, cached ou unknown.

Só interpretar `items: []` como ausência dentro da cobertura quando status, completude e paginação confirmarem. Distinguir zero observado, dado não informado e falha. Null em `frescor_max_min` não significa validade ilimitada. Calendário guarda compromissos; comunicação e documentos permanecem em seus aplicativos; o vault conserva referências e contexto mínimo.

## Efeito externo

Exigir pedido/delegação pertinente, alvo e destinatário resolvidos, conteúdo revisável, limites, precondição do objeto quando suportada e chave de idempotência do serviço quando houver. Retenha recibo remoto. Timeout deixa resultado desconhecido até consulta; não repita sem prova. Entrega no vault não é envio, envio não é leitura nem conclusão de tarefa.

## Módulo

Use `Templates/modulo.md` e o exemplo `Templates/modulo-estudos.json`. Um manifesto aplicado precisa de module_note_id real, versão, necessidade, tipos reutilizados, campos com namespace e tipos, sensibilidade, padrões, evidência, dependências sem ciclos, capacidades, limites, aceite, piloto, migração e saída. Campos especializados não duplicam status, prazo ou evidência do núcleo.

O exemplo de Estudos permanece modelo. Não há matrícula, progresso ou módulo pessoal ativo presumido. Novos acessos e custos exigem autorização separada. Pausar/desativar suspende procedimentos e disparadores especializados e conserva leitura; compromissos assumidos precisam de decisão explícita.

## Agendas

Agenda usa JSON separado da rotina: fuso IANA confirmado, recorrência, janela, política de atraso/DST, ID e estado remoto, canal, autorização e capacidade do executor. Não ativar arquivo com placeholders. O modelo não cria um disparador.

Chave de ocorrência: vault_id + rotina_id + slot/período + timezone + identificador da regra. Retry preserva chave; mudança de versão do procedimento não duplica o slot. Reserva e finalização exigem precondição e posse da tentativa. Resultado tardio de tentativa cancelada não substitui a vigente. Pausa confere nota e disparador real; retomada não recupera todos os atrasos.
