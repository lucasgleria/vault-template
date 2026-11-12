# Recuperação e retorno

## Escopo disponível

Em Git, use o histórico para recuperar revisões por novos commits. Em uma pasta ou serviço, verifique quais versões ou cópias estão disponíveis. A configuração de cópia independente, frequência, destino e retenção depende da escolha da pessoa e das ferramentas efetivas.

O auxiliar opcional `auxiliares/scripts/snapshot_archive.py` pode verificar exportação estável de um commit e restaurar em destino inexistente com `global_pause=true`. Não contém histórico Git, permissões, anexos externos ou credenciais; ZIP não é criptografia. O usuário diário não precisa executar esse programa.

## Procedimento por agente autorizado

1. Identificar o incidente e pausar as automações afetadas, tanto no vault quanto nos disparadores reais que estiverem configurados.
2. Preservar a revisão vigente e identificar explicitamente a origem e a revisão da cópia. Não eleger um clone como canônico.
3. Conferir inventário e hashes antes de preparar qualquer substituição. Corrupção bloqueia a recuperação.
4. Preparar estado em branch/destino separado de homologação. Manter `global_pause=true`.
5. Validar notas, relações, decisões, perfil, políticas, manifestos, recibos e amostras de conteúdo. Reconstruir índices derivados se existirem.
6. Comparar com o estado atual e preservar mudanças posteriores válidas. Reconciliar efeitos externos desde a revisão recuperada antes de repetir mensagens/eventos com recibos ausentes.
7. Aplicar o diff autorizado usando a proteção de versão disponível. Em Git, criar novo commit. Reler arquivos e confirmar presença no destino canônico.
8. Revalidar conexões e retomar somente capacidades escolhidas, sem recuperar todos os slots atrasados.

Uma restauração em branch de teste comprova o mecanismo e o escopo testado; não torna aquela branch um segundo vault em operação. Recuperação em outro repositório exige decisão explícita de migração e atualização das associações dos agentes.

## Cópia local opcional

Obsidian abre arquivos locais. Se escolhido, um mecanismo de sincronização deve conservar vault_id/IDs, preservar edições offline, obter o remoto, reconciliar por sentido, validar, enviar com controle de versão e confirmar a branch canônica. O clone permanece pendente enquanto offline; dois clones não compartilham lock. Nenhum plugin de sincronização foi instalado ou homologado.
