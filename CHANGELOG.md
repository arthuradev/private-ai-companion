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
- Avatar service com estados visuais, expressões, idle e lipsync.
- Provider fake de avatar para testes e bootstrap local.
- Adapter opt-in para VTube Studio via WebSocket API.
- Configuração versionável de avatar em `configs/avatar.default.toml`.
- CLI `--avatar-expression` para validar expressões sem depender do dashboard.
- Extra opcional `avatar` para instalar `websockets`.
- Vision service para contexto visual temporário com captura manual autorizada.
- Policy de captura de tela com bloqueio padrão de captura contínua, persistência
  de screenshot e análise externa.
- Redaction de metadados de texto visível antes da análise de visão.
- Providers fake locais para captura de tela e análise visual.
- Configuração versionável de privacidade em `configs/privacy.default.toml`.
- CLI `--screen-context` para validar contexto visual sem captura contínua.
- Eventos de visão sem bytes de screenshot ou texto visual cru.
- Safety pipeline para ações locais com classificação de risco, policy,
  confirmação, dry-run e audit log em memória.
- Desktop action service com port `DesktopActionExecutor`.
- Executor local seguro para notas locais, leitura simulada de título de janela
  e abertura simulada de apps permitidos.
- Configuração versionável de desktop em `configs/desktop.default.toml`.
- CLI `--desktop-action` com `--desktop-dry-run` e `--desktop-confirm`.
- Eventos `ActionIntentCreated`, `PermissionRequired`, `ActionExecuted` e
  `AuditEventCreated` sem parâmetros sensíveis.
- Sistema inicial de skills com manifests, registry, manager, policy e executor
  de efeitos governado.
- Skills embutidas `builtin.status`, `builtin.local_note` e
  `builtin.open_allowed_app`.
- Configuração versionável de skills em `configs/skills.default.toml`.
- CLI `--skill`, `--skill-input`, `--skill-dry-run`, `--skill-confirm` e
  `--skills-config`.
- Eventos `SkillInvoked`, `SkillDenied` e `SkillCompleted` sem input sensível.
- Testes de segurança garantindo que skills não bypassam o pipeline de ações.
- Dashboard local em Rich com status de runtime, configuração, memória,
  permissões de desktop e skills.
- Modelo local de tray/status com menu testável.
- CLI `--dashboard`, `--tray-status` e `--memory-config`.
- Bootstrap de memória conectado à aplicação para uso por UI e revisão local.
- Observabilidade local com logs estruturados em memória, métricas de eventos,
  replay sanitizado e health checks.
- Configuração versionável de observabilidade em
  `configs/observability.default.toml`.
- CLI `--diagnostics` e `--observability-config`.
- Teste de segurança garantindo que observabilidade não retém texto privado de
  turnos.
- `Start.bat` robustecido com logs de startup, detecção de `.env`, validação de
  Python 3.12+ e execução via `uv run --locked`.
- Script `scripts/release-check.ps1` para validações de release, build e launcher.
- Testes de contrato para launcher Windows, release-check e metadata do pacote.
- Script `scripts/final-audit.ps1` para hardening final, release-check, diff
  check e auditoria de artefatos privados.
- Testes finais de hardening para bloquear prompt operacional duplicado,
  artefatos runtime/build versionados, arquivos de segredo, dependências de
  streaming e logging de argumentos pelo launcher.
- Release estável Python `0.3.0`, correspondente à tag SemVer `v0.3.0`.

### Changed

- Removido `PROMPT-CODEX.md`, mantendo `AGENTS.md` e a documentação versionada
  como fonte de verdade para agentes.

### Fixed

- Nenhuma correção ainda.

## Release atual

- `0.3.0` / `v0.3.0`: dashboard/tray, observabilidade, empacotamento,
  release-check, launcher Windows robustecido e auditoria final da Fase 16.

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
