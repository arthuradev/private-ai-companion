# speech-config

## Responsabilidade

Configuração de microfone, VAD, STT, TTS, voz, idioma, fila de fala e interrupção.

## Arquivo padrão

A Fase 07 adiciona:

```text
configs/speech.default.toml
```

O arquivo é seguro para Git e não contém segredos. Ele configura TTS fake local,
STT fake local, VAD simples e playback fake/desabilitado para áudio real.

## Campos atuais

- `speech.tts.provider_id`: provider de TTS. Na Fase 07, apenas `fake-tts` é
  executável.
- `speech.tts.voice_id`: identificador de voz configurável.
- `speech.tts.language`: idioma principal da fala.
- `speech.tts.audio_format`: formato planejado do áudio.
- `speech.tts.enabled`: habilitação de TTS.
- `speech.playback.enabled`: habilitação de playback real planejado.
- `speech.playback.interrupt_on_new_input`: preferência de interrupção.
- `speech.stt.provider_id`: provider de STT. Na Fase 08, `fake-stt` e
  `faster-whisper` são reconhecidos.
- `speech.stt.language`: idioma preferencial da transcrição.
- `speech.stt.model_size`: tamanho do modelo planejado para `faster-whisper`.
- `speech.stt.device`: dispositivo planejado para `faster-whisper`, como `cpu`.
- `speech.stt.compute_type`: modo de computação planejado, como `int8`.
- `speech.stt.vad_filter`: habilita o VAD interno do `faster-whisper` quando
  esse provider estiver selecionado.
- `speech.stt.enabled`: habilita ou desabilita STT.
- `speech.input.mode`: modo de entrada. Valores atuais: `push-to-talk` ou `vad`.
- `speech.input.microphone_enabled`: permanece `false` por padrão; não há
  captura contínua de microfone na Fase 08.
- `speech.input.vad_enabled`: aplica VAD antes de transcrever clipes explícitos.
- `speech.input.vad_threshold`: limiar do VAD simples usado no bootstrap/testes.
- `speech.input.max_record_seconds`: limite planejado para gravação PTT futura.

## Privacidade e performance

- A Fase 08 processa apenas clipes explícitos, como `--voice-file`.
- O microfone real fica desabilitado por padrão.
- `fake-stt` não chama rede e não usa modelo externo.
- `faster-whisper` é local, mas pode baixar/carregar modelos e consumir CPU/GPU;
  instale com `uv sync --extra stt` antes de selecionar esse provider.

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
