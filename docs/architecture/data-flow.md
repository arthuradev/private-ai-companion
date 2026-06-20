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
→ Autorização explícita
→ ScreenCaptureProvider
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
→ DesktopPermissionPolicy
→ DryRun
→ ConfirmationGate
→ DesktopActionExecutor
→ ActionExecuted
→ InMemoryActionAuditLog
```

## Skill com efeito local

```text
Usuário ou serviço interno solicita skill
→ SkillRequest
→ SkillInvoked
→ SkillPolicy
→ BaseSkill.invoke
→ SkillEffectRequest
→ DesktopSkillEffectExecutor
→ pipeline de Ação local
→ SkillCompleted
→ SkillRunResult
```

Uma skill não executa comandos diretamente. Quando o efeito representa ação de
desktop, ele entra no mesmo fluxo de risco, dry-run, confirmação, execução e
auditoria das ações locais.

## Dashboard e tray local

```text
Usuário solicita dashboard ou tray status
→ Entry point oficial
→ Application bootstrap
→ DashboardSnapshot
→ RichDashboardApp ou RichTrayStatusApp
→ renderização local
→ shutdown do modo pontual
```

A UI complementar lê serviços públicos da aplicação e renderiza estado. Ela não
executa actions, não acessa banco de memória diretamente e não bypassa policy.

## Observabilidade e diagnóstico

```text
Módulos publicam eventos
→ EventBus
→ ObservabilityService
→ sanitize_event
→ StructuredEventLogger / EventReplayRecorder / EventMetricsCollector
→ HealthCheckService
→ DiagnosticsSnapshot
→ RichDiagnosticsApp
```

Logs e replay são sanitizados antes de retenção. Texto de conversa, conteúdo
visual, parâmetros completos de ações e segredos não entram em diagnóstico por
padrão.
