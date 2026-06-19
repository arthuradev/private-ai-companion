# Ports and Adapters

## Objetivo

Permitir que o projeto troque provedores e tecnologias sem reescrever o núcleo.

## Ports planejados

- `LLMProvider`
- `STTProvider`
- `TTSProvider`
- `AvatarProvider`
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
