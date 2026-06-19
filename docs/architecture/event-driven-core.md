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
