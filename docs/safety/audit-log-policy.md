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
