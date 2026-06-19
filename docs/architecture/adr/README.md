# Architecture Decision Records

Esta pasta contém ADRs do projeto.

## Regras

- ADRs aceitas não devem ser reescritas para apagar histórico.
- Se uma decisão mudar, crie uma nova ADR substituindo a anterior.
- ADRs devem ser curtas e objetivas.

## Template

```md
# ADR-XXXX — Título

## Status

Accepted | Superseded | Proposed

## Contexto

...

## Decisão

...

## Consequências

...
```

## ADRs incluídas após alinhamento de launcher

- `0015-use-start-bat-as-windows-friendly-entrypoint.md`: define `Start.bat` como entrypoint amigável para Windows, sem transformar o launcher em núcleo do produto.
