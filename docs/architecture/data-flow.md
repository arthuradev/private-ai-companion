# Fluxos de Dados

## Conversa por texto

```text
Usuário digita
→ UserTextReceived
→ Interaction Layer
→ ContextBuilder
→ MemoryRetriever
→ PromptBuilder
→ LLMRouter
→ ResponsePlanner
→ AssistantTextReady
→ EmotionPlanner
→ AvatarStateRequested
→ MemoryCandidateCreated
→ UI render
```

## Conversa por voz

```text
Microfone
→ VAD
→ STT
→ UserSpeechReceived
→ Pipeline de texto
→ TTSRequested
→ SpeechQueue
→ AudioPlayer
→ AvatarLipSync
```

## Visão de tela

```text
Usuário solicita contexto visual
→ ScreenCapturePolicy
→ PermissionManager
→ ScreenshotService
→ Redactor
→ VisionProvider
→ TemporaryVisualContext
→ PromptBuilder
→ descarte ou retenção controlada
```

## Ação local

```text
LLM sugere ActionIntent
→ schema validation
→ RiskClassifier
→ ActionPolicy
→ DryRun
→ ConfirmationGate
→ SafeExecutor
→ PostValidation
→ AuditLog
```
