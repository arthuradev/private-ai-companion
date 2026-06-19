# Event-driven Core

## Objetivo

Separar entrada, processamento e saída usando eventos internos.

## Benefícios

- reduz acoplamento;
- facilita logs/replay;
- permite múltiplas interfaces;
- melhora testabilidade;
- facilita interrupção de voz/avatar;
- permite observabilidade.

## Eventos principais

- `AppStarted`
- `AppStopping`
- `AppStopped`
- `UserTextReceived`
- `VoiceInputStarted`
- `UserSpeechReceived`
- `VoiceInputIgnored`
- `VoiceInputFinished`
- `AssistantResponseRequested`
- `AssistantTextReady`
- `TTSRequested`
- `SpeechStarted`
- `SpeechFinished`
- `SpeechInterrupted`
- `AvatarStateRequested`
- `AvatarStateApplied`
- `AvatarLipsyncUpdated`
- `MemoryCandidateCreated`
- `MemoryCommitted`
- `ScreenContextRequested`
- `ScreenContextCaptured`
- `ScreenContextDenied`
- `ScreenContextRedacted`
- `VisionAnalysisReady`
- `ActionIntentCreated`
- `PermissionRequired`
- `ActionExecuted`
- `AuditEventCreated`
- `SkillInvoked`
- `SkillDenied`
- `SkillCompleted`

## Regra

Eventos não devem carregar segredos nem payloads privados sem classificação de sensibilidade.

## Estado na Fase 02

A Fase 02 implementa a base do core orientado a eventos:

- `BaseEvent` e `EventMetadata`;
- classificação inicial de sensibilidade de eventos;
- eventos de lifecycle `AppStarted`, `AppStopping` e `AppStopped`;
- `EventBus` assíncrono em memória;
- `RuntimeStateStore` com transições de lifecycle controladas;
- `LifecycleManager` e `CoreOrchestrator`.

## Estado na Fase 03

A Fase 03 adiciona os eventos de texto:

- `UserTextReceived`;
- `AssistantTextReady`.

Esses eventos são usados pela interação local de texto. Eventos de voz, avatar,
memória, visão, ações e audit log continuam como contratos planejados para fases
futuras.

## Estado na Fase 07

A Fase 07 adiciona os eventos de fala:

- `TTSRequested`;
- `SpeechStarted`;
- `SpeechFinished`;
- `SpeechInterrupted`.

Esses eventos são usados pela fila de fala e pelo fluxo fake de TTS/playback.

## Estado na Fase 08

A Fase 08 adiciona os eventos de entrada de voz:

- `VoiceInputStarted`;
- `UserSpeechReceived`;
- `VoiceInputIgnored`;
- `VoiceInputFinished`.

`UserSpeechReceived` carrega a transcrição e deve usar sensibilidade `private`.
Eventos de ciclo de voz não carregam bytes de áudio.

## Estado na Fase 09

A Fase 09 adiciona os eventos de avatar:

- `AvatarStateRequested`;
- `AvatarStateApplied`;
- `AvatarLipsyncUpdated`.

Esses eventos representam estado visual e lipsync. Eles não carregam imagem,
modelo Live2D ou token do VTube Studio.

## Estado na Fase 10

A Fase 10 adiciona os eventos de visão:

- `ScreenContextRequested`;
- `ScreenContextCaptured`;
- `ScreenContextDenied`;
- `ScreenContextRedacted`;
- `VisionAnalysisReady`.

Esses eventos carregam apenas identificadores, status, dimensões e contagens.
Eles não carregam bytes de screenshot, texto visual cru ou resumo sensível.

## Estado na Fase 11

A Fase 11 adiciona os eventos de ações locais:

- `ActionIntentCreated`;
- `PermissionRequired`;
- `ActionExecuted`;
- `AuditEventCreated`.

Esses eventos carregam apenas ids, tipo de ação, risco, status e decisão. Eles
não carregam parâmetros da ação, corpo de nota, comandos, segredos ou conteúdo
privado.

## Estado na Fase 12

A Fase 12 adiciona os eventos de skills:

- `SkillInvoked`;
- `SkillDenied`;
- `SkillCompleted`.

Esses eventos carregam apenas skill id, request id, source, motivo de negação,
status e contagem de efeitos. Eles não carregam input da skill, parâmetros dos
efeitos, corpo de nota, segredos ou conteúdo privado.
