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
- `UserSpeechReceived`
- `AssistantResponseRequested`
- `AssistantTextReady`
- `TTSRequested`
- `SpeechStarted`
- `SpeechFinished`
- `SpeechInterrupted`
- `AvatarStateRequested`
- `MemoryCandidateCreated`
- `MemoryCommitted`
- `ScreenContextRequested`
- `ActionIntentCreated`
- `PermissionRequired`
- `ActionExecuted`
- `AuditEventCreated`

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
Entrada por voz ainda fica para a Fase 08.
