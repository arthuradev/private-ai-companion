# C4 Context

## Sistema

`private-ai-companion` é uma aplicação desktop local-first para companion AI privada.

## Pessoas

- Usuário final.
- Desenvolvedor/contribuidor.
- Agente de IA implementador.

## Sistemas externos

- Provedores LLM cloud.
- Provedores LLM locais.
- Provedores STT/TTS.
- VTube Studio/Live2D.
- Sistema operacional.
- GitHub.

## Diagrama textual

```text
[User]
  └── uses ──> [private-ai-companion]
                  ├── optionally calls ──> [Cloud LLM Providers]
                  ├── optionally calls ──> [Cloud TTS/STT Providers]
                  ├── integrates ────────> [VTube Studio]
                  ├── stores locally ────> [SQLite]
                  └── observes/acts ─────> [Desktop OS with Policy]
```
