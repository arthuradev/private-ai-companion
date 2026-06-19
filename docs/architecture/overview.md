# Visão Geral da Arquitetura

`private-ai-companion` é um monólito modular local-first orientado a eventos.

## C4 — Contexto

```text
Usuário
  ↓
private-ai-companion
  ↔ Provedores LLM locais/cloud
  ↔ Provedores STT/TTS
  ↔ VTube Studio / Live2D
  ↔ Sistema operacional desktop
  ↔ Banco SQLite local
```

## C4 — Containers internos

```text
CLI / Tray / Dashboard
Interaction Layer
Core Runtime
Brain
Memory
Speech
Avatar
Vision
Desktop
Safety
Skills
Observability
```

## Fluxo principal

```text
Entrada do usuário
→ evento
→ orquestrador
→ contexto/persona/memória
→ LLM router
→ planejador de resposta
→ planejador emocional
→ saída multimodal
→ memória/audit/logs
```

## Por que monólito modular?

Microserviços seriam complexidade artificial para um app desktop. Um monólito sem fronteiras viraria bagunça. O monólito modular permite uma única aplicação com limites internos fortes.
