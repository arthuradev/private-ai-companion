# ARCHITECTURE.md

## 1. Visão geral

`private-ai-companion` usa uma arquitetura de monólito modular local-first, orientada a eventos, com ports/adapters e safety/privacy engine.

O projeto deve crescer como uma aplicação única, mas internamente dividida em módulos com responsabilidades claras.

## 2. Filosofia

A arquitetura responde às perguntas:

- O que é central e não pode quebrar?
- O que pode ser plugado/removido?
- Quem pode chamar quem?
- Onde ficam APIs externas?
- Onde ficam dados privados?
- Como uma ação perigosa é validada?
- Como uma IA futura entende o sistema?

## 3. Núcleo

O núcleo deve conter apenas:

- eventos;
- event bus;
- orquestração;
- ciclo de vida;
- estado de runtime;
- contratos;
- erros e resultados.

O núcleo não deve conhecer:

- OpenAI, Anthropic, Gemini, Ollama, OpenRouter;
- ElevenLabs, Piper, EdgeTTS;
- faster-whisper;
- VTube Studio;
- SQLite diretamente quando evitável;
- Windows APIs específicas;
- Rich/Pyfiglet;
- dashboard/tray.

## 4. Módulos principais

```text
core/          runtime, eventos, orquestração
interaction/   turnos, entrada/saída, interrupção
brain/         persona, prompt builder, LLM router, emotion planner
memory/        SQLite, política, sumarização, busca
speech/        VAD, STT, TTS, fila de fala, playback
avatar/        estado visual, expressões, lipsync, adapters
vision/        screenshot, contexto visual, redaction, policy
desktop/       janela ativa, apps permitidos, ações locais seguras
safety/        risco, privacidade, permissões, dry-run, audit
skills/        capacidades opcionais e manifests
ui/            CLI, tray, dashboard
config/        carregamento e validação de configuração
observability/ logs, métricas, replay, health checks
```

## 5. Diagrama conceitual

```text
User Input
  ↓
UI / Speech / Desktop Event
  ↓
Interaction Layer
  ↓
Core Orchestrator + Event Bus
  ↓
Brain + Memory + Safety
  ↓
Output Router
  ↓
Text / TTS / Avatar / Skill / Desktop Action
```

## 6. Regras de dependência

- `core/` não importa `ui/`, `speech/`, `avatar/`, `desktop/`, `vision/` ou providers concretos.
- `brain/` não executa ações locais diretamente.
- `memory/` não decide sozinho o que é seguro lembrar.
- `avatar/` não chama LLM.
- `speech/` não conhece desktop automation.
- `vision/` não persiste imagens sem policy.
- `desktop/` não executa ações sem `safety/`.
- `skills/` passam por registry, permissions e policy.
- `ui/` não contém regra de negócio.
- LLMs produzem sugestões; políticas determinísticas decidem.

## 7. Ports and adapters

O projeto deve expor contratos internos para:

- LLM providers;
- STT providers;
- TTS providers;
- avatar providers;
- vision providers;
- memory stores;
- desktop actions;
- skills.

Cada implementação concreta deve ficar em adapter/provider apropriado.

## 8. Event-driven core

Comunicação entre módulos deve ocorrer preferencialmente por eventos.

Eventos esperados:

- `UserTextReceived`
- `UserSpeechReceived`
- `AssistantTextReady`
- `TTSRequested`
- `SpeechStarted`
- `SpeechInterrupted`
- `AvatarStateRequested`
- `MemoryCandidateCreated`
- `ActionIntentCreated`
- `PermissionRequired`
- `ScreenContextRequested`

## 9. Avatar

O avatar é uma camada de apresentação. Ele reflete estados como:

- idle;
- listening;
- thinking;
- speaking;
- interrupted;
- happy;
- curious;
- concerned;
- confused.

## 10. Segurança

Ações locais seguem pipeline:

```text
ActionIntent
→ RiskClassification
→ PolicyDecision
→ DryRun
→ ConfirmationGate
→ Execution
→ PostValidation
→ AuditLog
```

## 11. Evitando main gigante

`__main__.py` deve apenas iniciar o app. O bootstrap monta dependências. O orquestrador coordena eventos. Regras vivem em módulos especializados.

Nenhum arquivo deve virar centro informal do sistema.

## 12. Startup launcher

O projeto deve possuir um entrypoint amigável para usuários finais no Windows, preferencialmente `Start.bat`.

O launcher pertence à borda operacional do sistema. Ele pode preparar ambiente e chamar o entrypoint Python oficial, mas não deve conter regra de negócio, lógica de LLM, memória, avatar, voz, visão ou ações locais.

Fluxo esperado:

```text
Start.bat
→ valida ambiente
→ prepara dependências
→ chama entrypoint Python oficial
→ bootstrap/app_factory
→ core/runtime
```

O núcleo não deve depender do `Start.bat`. O `Start.bat` é apenas uma forma conveniente de iniciar o sistema.
