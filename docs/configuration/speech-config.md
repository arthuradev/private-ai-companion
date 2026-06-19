# speech-config

## Responsabilidade

Configuração de microfone, VAD, STT, TTS, voz, idioma, fila de fala e interrupção.

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
