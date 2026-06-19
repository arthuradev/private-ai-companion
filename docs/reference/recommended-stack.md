# Stack Recomendada

## Base

- Python 3.12+
- uv
- ruff
- pytest
- pyright
- pydantic
- SQLite

## UI

- Rich
- Pyfiglet
- Tray/dashboard em fase posterior

## LLM

- Router híbrido
- OpenAI-compatible provider
- OpenAI
- Anthropic
- Gemini
- OpenRouter
- Ollama
- LM Studio
- DeepSeek
- xAI/Grok

## STT

- faster-whisper como base local.

## TTS

- ElevenLabs como opção premium.
- Adapters para OpenAI TTS, Piper, EdgeTTS e outros.

## Avatar

- VTube Studio + Live2D inicialmente.
- Adapter abstrato para alternativas futuras.
- `websockets` como dependência opcional para o adapter VTube Studio.

## Visão

- Provider fake/local como default seguro.
- Adapters reais de captura e análise visual devem ser opt-in e passar por
  policy de privacidade antes de observar ou enviar screenshots.
