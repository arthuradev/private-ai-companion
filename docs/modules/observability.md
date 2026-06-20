# Módulo `observability`

## Responsabilidade

Gerencia logs estruturados, métricas, health checks, traces e replay de eventos.

## Implementado na Fase 14

- `ObservabilityService` assina o `EventBus` e registra eventos publicados.
- `EventReplayRecorder` mantém replay sanitizado em memória.
- `StructuredEventLogger` produz logs estruturados em memória.
- `EventMetricsCollector` conta eventos por nome, source e sensibilidade.
- `HealthCheckService` executa checks locais de runtime, LLM, memória, avatar,
  visão, desktop e skills.
- `RichDiagnosticsApp` renderiza diagnóstico local via `--diagnostics`.
- `configs/observability.default.toml` controla retenção e componentes ativos.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.
- Não deve persistir payload privado por padrão.
- Não deve depender de UI, adapters ou providers concretos.
- Deve redigir campos sensíveis antes de logs e replay.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- Contratos de outros módulos, quando necessário.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.
- `DiagnosticsSnapshot` com health report, métricas, replay sanitizado e logs
  estruturados.

## Sanitização

Campos como `text`, `content`, `summary`, `purpose`, `parameters`, `title`,
`body`, `visible_text` e `prompt` são removidos dos registros de observabilidade.

Eventos com sensibilidade `private` ou `sensitive` mantêm apenas campos
operacionais permitidos, como ids, status, tipo de ação, risco, provider,
contagens e flags. Isso permite diagnóstico sem registrar conversa completa,
screenshots, parâmetros de ação ou segredos.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
- Usar logs como armazenamento permanente de conversa.
- Implementar replay com payload bruto.
