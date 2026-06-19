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

## Desktop actions

- Executor local seguro como default.
- Abertura real de apps, automação de janela, clipboard e arquivos devem ser
  opt-in e passar por risk policy, dry-run, confirmação e audit log.

## Skills

- Manifests tipados e versionados para cada skill.
- Registry em memória para skills embutidas e futuras extensões.
- Manager governado por policy antes de invocar skills.
- Efeitos representados como requests estruturados e executados por ports.
- Nenhuma skill deve chamar shell, rede, filesystem amplo ou providers externos
  sem adapter, policy e consentimento explícito.
