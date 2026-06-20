# observability-config

## Responsabilidade

Configuração de logs estruturados, métricas, replay sanitizado de eventos e
health checks.

## Arquivo padrão

```text
configs/observability.default.toml
```

O arquivo é seguro para Git e não contém dados privados. A Fase 14 mantém logs e
replay em memória por padrão. Persistência em arquivo/exportação deve continuar
opt-in e redigida em fases futuras.

## Campos atuais

- `enabled`: habilita observabilidade como um todo.
- `structured_logging_enabled`: registra eventos em logs estruturados em memória.
- `max_log_records`: retenção máxima de registros estruturados em memória.
- `event_replay_enabled`: habilita replay sanitizado de eventos.
- `max_replay_events`: retenção máxima de eventos sanitizados em memória.
- `metrics_enabled`: coleta contadores por evento, source e sensibilidade.
- `health_checks_enabled`: habilita health checks locais.

## Privacidade

A sanitização é determinística e não possui flag pública para desligar na Fase
14. Campos como `text`, `content`, `summary`, `purpose`, `parameters`, `title`,
`body` e `visible_text` são redigidos antes de logs e replay.

Eventos privados ou sensíveis retêm apenas campos operacionais permitidos, como
ids, status, tipo de ação, risco, provider id, contagens e flags.

## CLI

```text
uv run private-ai-companion --observability-config configs/observability.default.toml --diagnostics
```

No Windows:

```text
Start.bat --observability-config configs/observability.default.toml --diagnostics
```
