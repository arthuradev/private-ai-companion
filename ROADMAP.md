# ROADMAP.md

## Visão

Construir uma companion AI privada, open-source e modular para desktop, com voz, avatar, memória local, visão autorizada, ações seguras e personalização simples.

## Marco 0 — Base documental

- Documentação inicial completa.
- ADRs iniciais.
- Plano de fases.
- Regras para Codex.

## Marco 1 — Fundação técnica

- Projeto Python 3.12+.
- `uv`, `ruff`, `pytest`, `pyright`.
- Estrutura `src/`.
- Configuração inicial.
- Logs e health checks básicos.

## Marco 2 — Runtime e conversa por texto

- Event bus.
- Orquestrador.
- CLI Rich/Pyfiglet.
- Interação por texto.
- Persona configurável.
- Prompt builder.

## Marco 3 — LLM router e memória

- LLM router híbrido.
- Provider fake para testes.
- Providers cloud/local.
- SQLite.
- Memory policy.
- Memória editável/auditável.

## Marco 4 — Voz

- TTS adapters.
- Fila de fala.
- Interrupção.
- STT com faster-whisper.
- Entrada por voz.

## Marco 5 — Avatar

- VTube Studio adapter.
- Estados visuais.
- Expressões.
- Lipsync.
- Idle behavior.

## Marco 6 — Visão e desktop seguro

- Screenshot autorizado.
- Janela ativa.
- Contexto visual temporário.
- Ações locais permitidas.
- Risk policy.
- Dry-run e audit log.

## Marco 7 — Skills/plugins

- Skill manifest.
- Skill registry.
- Skill manager.
- Skills iniciais: notas, lembretes, app launcher, busca web, avatar control.

## Marco 8 — UI complementar e release

- Tray app.
- Dashboard local.
- Painel de memória/permissões.
- Empacotamento.
- Release `v0.1.0` quando conversa funcional com voz, memória e avatar estiver concluída.

## Futuro

- Overlay próprio.
- Live2D Web próprio.
- RAG avançado.
- Embeddings locais.
- Voice full-duplex.
- Mais provedores locais.
- Marketplace/comunidade de skills.

## Requisito transversal — inicialização amigável

O projeto deve manter um caminho amigável de inicialização para Windows por `Start.bat`. Esse requisito atravessa fundação, CLI, empacotamento e release. Comandos técnicos podem existir, mas não substituem o launcher para usuário final.
