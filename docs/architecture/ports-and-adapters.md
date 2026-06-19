# Ports and Adapters

## Objetivo

Permitir que o projeto troque provedores e tecnologias sem reescrever o núcleo.

## Ports planejados

- `LLMProvider`
- `STTProvider`
- `TTSProvider`
- `AvatarProvider`
- `ScreenCaptureProvider`
- `VisionProvider`
- `MemoryStore`
- `DesktopActionExecutor`
- `Skill`
- `ConfigProvider`

## Adapters planejados

- OpenAI
- Anthropic
- Gemini
- OpenRouter
- Ollama
- LM Studio
- DeepSeek
- xAI/Grok
- faster-whisper
- ElevenLabs
- Piper
- EdgeTTS
- VTube Studio
- SQLite
- Fake screen capture
- Fake vision
- Safe local desktop executor

## Regra

Adapters podem ser feios; o núcleo não. Código específico de API, sistema operacional ou biblioteca deve ficar nas bordas.

## Estado na Fase 05

O primeiro port implementado é `LLMProvider`, dentro de `brain/`.

O primeiro adapter concreto é:

```text
src/private_ai_companion/adapters/llm/fake.py
```

Ele é local, determinístico, não chama rede e serve para testes, bootstrap e
desenvolvimento até que adapters reais sejam implementados em fases futuras.

## Estado na Fase 07

A Fase 07 adiciona os ports de fala:

- `TTSProvider`;
- `AudioPlayer`.

Adapters concretos fake:

```text
src/private_ai_companion/adapters/speech/fake_tts.py
src/private_ai_companion/adapters/speech/fake_audio.py
```

Eles não chamam APIs externas e não acessam dispositivo de áudio real.

## Estado na Fase 08

A Fase 08 adiciona os ports de entrada de voz:

- `STTProvider`;
- `VoiceActivityDetector`;
- `PushToTalkRecorder`.

Adapters concretos:

```text
src/private_ai_companion/adapters/speech/fake_stt.py
src/private_ai_companion/adapters/speech/faster_whisper_stt.py
src/private_ai_companion/adapters/speech/simple_vad.py
```

`FakeSTTProvider` e `EnergyVoiceActivityDetector` são locais e determinísticos.
`FasterWhisperSTTProvider` é opt-in e importa `faster-whisper` apenas quando o
provider é usado. O core não conhece `faster-whisper`.

## Estado na Fase 09

A Fase 09 adiciona o port de avatar:

- `AvatarProvider`.

Adapters concretos:

```text
src/private_ai_companion/adapters/avatar/fake_avatar.py
src/private_ai_companion/adapters/avatar/vtube_studio.py
```

`FakeAvatarProvider` é local e determinístico. `VTubeStudioAvatarProvider` é
opt-in, usa a WebSocket API pública local do VTube Studio e importa `websockets`
apenas quando o provider real é usado.

O adapter VTube Studio usa:

- `AuthenticationTokenRequest` / `AuthenticationRequest` para autorização;
- `HotkeyTriggerRequest` para expressões configuradas como hotkeys;
- `InjectParameterDataRequest` para lipsync por parâmetro configurável.

## Estado na Fase 10

A Fase 10 adiciona os ports de visão:

- `ScreenCaptureProvider`;
- `ImageRedactor`;
- `VisionProvider`.

Adapters concretos fake:

```text
src/private_ai_companion/adapters/vision/fake_capture.py
src/private_ai_companion/adapters/vision/fake_vision.py
```

`FakeScreenCaptureProvider` e `FakeVisionProvider` são locais, determinísticos e
não chamam rede. O fluxo completo passa por `ScreenCapturePolicy` antes de
captura ou análise. O core não conhece providers de visão concretos.

## Estado na Fase 11

A Fase 11 adiciona o port de desktop:

- `DesktopActionExecutor`.

Adapter concreto:

```text
src/private_ai_companion/adapters/desktop/safe_local.py
```

`SafeLocalDesktopExecutor` é local e seguro por padrão. Ele cria notas apenas no
diretório configurado, simula abertura de apps allowlisted e não chama shell,
mouse, teclado ou APIs externas. O fluxo completo passa por `RiskClassifier`,
`ActionPolicy`, `DesktopPermissionPolicy`, dry-run, confirmação e audit log.
