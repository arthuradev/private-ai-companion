# Política de Audit Log

## Objetivo

Registrar decisões e ações sem vazar dados privados.

## Deve registrar

- Tipo de ação.
- Risco.
- Resultado da policy.
- Confirmação exigida.
- Execução ou bloqueio.
- Erro classificado.
- Timestamp.

## Não deve registrar por padrão

- Conversa completa.
- Screenshot bruto.
- Segredos.
- Conteúdo integral de arquivos privados.
- Parâmetros completos de ações locais.

## Estado na Fase 11

`InMemoryActionAuditLog` registra:

- id de auditoria;
- id e tipo da ação;
- risco;
- decisão da policy;
- resultado;
- se confirmação era exigida;
- se houve execução;
- timestamp.

Na Fase 11 o audit log é em memória. Persistência estruturada e exportação devem
ser tratadas junto com observabilidade em fase posterior.

## Estado na Fase 14

A observabilidade adiciona logs estruturados e replay de eventos em memória, com
sanitização antes de retenção. Esses registros são diagnósticos, não substituem o
audit log de ações locais.

Por padrão, observabilidade não registra:

- texto completo do usuário;
- resposta textual gerada;
- parâmetros completos de ações;
- corpo de nota;
- propósito de captura de tela;
- screenshot, texto visual cru ou conteúdo de arquivos.

O modo `--diagnostics` mostra health checks, métricas, replay sanitizado e
resumo de logs estruturados para depuração local.
