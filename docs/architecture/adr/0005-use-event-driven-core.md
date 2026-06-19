# ADR-0005 — Use event-driven core

## Status

Accepted

## Contexto

Texto, voz, avatar, memória e ações têm fluxos assíncronos.

## Decisão

O core usará event bus interno para coordenar módulos.

## Consequências

Reduz acoplamento e facilita replay/logs, mas exige disciplina em eventos.
