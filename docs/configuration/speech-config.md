# speech-config

## Responsabilidade

Configuração de microfone, VAD, STT, TTS, voz, idioma, fila de fala e interrupção.

## Arquivo padrão

A Fase 07 adiciona:

```text
configs/speech.default.toml
```

O arquivo é seguro para Git e não contém segredos. Ele configura apenas TTS fake
local e playback fake/desabilitado para áudio real.

## Campos atuais

- `speech.tts.provider_id`: provider de TTS. Na Fase 07, apenas `fake-tts` é
  executável.
- `speech.tts.voice_id`: identificador de voz configurável.
- `speech.tts.language`: idioma principal da fala.
- `speech.tts.audio_format`: formato planejado do áudio.
- `speech.tts.enabled`: habilitação de TTS.
- `speech.playback.enabled`: habilitação de playback real planejado.
- `speech.playback.interrupt_on_new_input`: preferência de interrupção.

## Regras

- Configuração versionável não deve conter segredos.
- Valores sensíveis devem vir de `.env` ou armazenamento seguro.
- Configurações devem ser validadas por modelos tipados.
- Defaults devem ser seguros para projeto público.
- O usuário deve conseguir personalizar sem alterar código.

## Deve documentar

- campos disponíveis;
- valores padrão;
- exemplos seguros;
- impacto de privacidade;
- impacto de performance;
- fallback quando ausente.
