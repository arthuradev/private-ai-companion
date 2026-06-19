# Módulo `speech`

## Responsabilidade

Gerencia microfone, VAD, STT, TTS, fila de fala, audio player e interrupção.

## Implementado na Fase 07

- Contratos `TTSProvider` e `AudioPlayer`.
- Modelos tipados de request TTS, áudio sintetizado, item de fila e interrupção.
- Fila de fala com drain controlado e interrupção.
- Adapter fake de TTS.
- Audio player fake para testes e bootstrap.
- Eventos `TTSRequested`, `SpeechStarted`, `SpeechFinished` e
  `SpeechInterrupted`.

Ainda não há reprodução de áudio real ou provider externo de TTS. Esses itens
continuam para fases futuras.

## Implementado na Fase 08

- Contratos `STTProvider`, `VoiceActivityDetector` e `PushToTalkRecorder`.
- Modelos tipados para clipe de entrada, request/result de STT, segmentos,
  resultado de VAD e resultado de entrada por voz.
- `VoiceInputService` para processar clipes explícitos, aplicar VAD opcional,
  transcrever e publicar eventos sem carregar bytes de áudio nos eventos.
- `VoiceInteractionService` para transformar transcrição de voz em turno normal
  de texto.
- Adapter `FakeSTTProvider` local e determinístico.
- Adapter `FasterWhisperSTTProvider` opt-in, com import preguiçoso de
  `faster-whisper`.
- `EnergyVoiceActivityDetector` simples para testes e bootstrap.
- CLI `--voice-file` para validar entrada por voz a partir de arquivo explícito.
- Eventos `VoiceInputStarted`, `UserSpeechReceived`, `VoiceInputIgnored` e
  `VoiceInputFinished`.

O microfone real permanece desabilitado por padrão. A Fase 08 não introduz
captura contínua de áudio; o fluxo atual processa clipes explícitos e mantém a
captura real de microfone para uma evolução futura controlada por policy/config.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- Contratos de outros módulos, quando necessário.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
