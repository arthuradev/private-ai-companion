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
