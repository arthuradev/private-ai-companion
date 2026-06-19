# CHANGELOG.md

Este projeto segue o espírito do Keep a Changelog e usa versionamento SemVer.

## [Unreleased]

### Added

- Base documental inicial do projeto.
- Planejamento de arquitetura modular.
- Plano de fases para implementação pelo Codex.
- Políticas iniciais de segurança, privacidade, memória e ações.
- ADRs iniciais.
- Fundação Python 3.12+ com `src/`, `uv`, `ruff`, `pytest` e `pyright`.
- Entry point oficial `private-ai-companion`.
- `Start.bat` inicial para usuários Windows.
- Testes iniciais de sanidade e boundary arquitetural.
- Runtime central com event bus, lifecycle, orquestrador e estado de runtime.
- Bootstrap inicial para montar a aplicação a partir do pacote Python.
- CLI inicial com Rich/Pyfiglet.
- Conversa por texto local da Fase 03, sem LLM ou memória permanente.
- Eventos `UserTextReceived` e `AssistantTextReady`.
- Persona configurável por `configs/persona.default.toml`.
- Loader tipado de configuração de persona.
- Context builder e prompt builder estruturado.
- Testes de prompt, persona config e boundaries de `brain`/`config`.
- LLM router com fallback e contratos de provider.
- Provider fake local para testes e desenvolvimento.
- Configuração versionável de providers em `configs/providers.default.toml`.
- Providers locais/cloud planejados, desabilitados por padrão e sem segredos.
- Memória local SQLite com repository, schema e audit log de decisões.
- Policy de memória com rejeição padrão de conteúdo sensível.
- Serviço de revisão para aprovar, rejeitar, editar e apagar memórias.
- Configuração versionável de memória em `configs/memory.default.toml`.
- TTS fake local e contratos de provider/player.
- Fila de fala com eventos `TTSRequested`, `SpeechStarted`, `SpeechFinished` e
  `SpeechInterrupted`.
- Interrupção de fala com limpeza da fila e cancelamento do item atual.
- Configuração versionável de speech em `configs/speech.default.toml`.
- STT fake local para testes e desenvolvimento.
- Adapter opt-in para `faster-whisper` com import preguiçoso.
- VAD simples por energia de bytes para clipes explícitos.
- Entrada por voz com eventos `VoiceInputStarted`, `UserSpeechReceived`,
  `VoiceInputIgnored` e `VoiceInputFinished`.
- CLI `--voice-file` para validar transcrição de arquivo explícito sem captura
  contínua de microfone.
- Extra opcional `stt` para instalar `faster-whisper`.

### Changed

- Nenhuma mudança ainda.

### Fixed

- Nenhuma correção ainda.

## Versionamento planejado

- `v0.1.0`: primeira versão funcional com conversa, voz, memória e avatar.
- `v0.2.0`: visão de tela, ações locais seguras e skills iniciais.
- `v0.3.0`: dashboard/tray, empacotamento e hardening.
- `v1.0.0`: versão estável pública após auditoria, documentação completa e segurança revisada.

## [Documentação] — Requisito de Start.bat

- Registrado requisito de launcher amigável para usuários Windows.
- Adicionado ADR sobre `Start.bat` como entrypoint operacional.
- Adicionada documentação de startup e launcher em `docs/runtime/startup-launcher.md`.
- Atualizadas fases de fundação, CLI e release para validar inicialização sem comandos técnicos.
