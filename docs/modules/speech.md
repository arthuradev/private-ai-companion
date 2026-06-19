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

Ainda não há STT, VAD, reprodução de áudio real ou provider externo de TTS.
Esses itens continuam para fases futuras.

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
