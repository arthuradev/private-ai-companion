# privacy-config

## Responsabilidade

Configuração de privacidade, envio para cloud, screenshots, logs, redaction e permissões.

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

## Estado na Fase 10

A configuração versionável padrão fica em:

```text
configs/privacy.default.toml
```

Campos atuais:

- `privacy.screen_capture.enabled`: habilita o fluxo de contexto visual.
- `privacy.screen_capture.provider_id`: provider de captura. Na Fase 10, apenas
  `fake-screen-capture` é executável.
- `privacy.screen_capture.require_user_authorization`: exige autorização humana
  por solicitação.
- `privacy.screen_capture.allow_continuous_capture`: controla captura contínua.
  O default é `false`.
- `privacy.screen_capture.persist_screenshots_by_default`: controla persistência
  de screenshots. O default é `false`.
- `privacy.screen_capture.allow_external_analysis`: controla envio para análise
  externa. O default é `false`.
- `privacy.redaction.enabled`: habilita redaction.
- `privacy.redaction.redact_text_metadata`: aplica redaction em metadados de
  texto visível antes da análise.
- `privacy.vision.provider_id`: provider de análise visual. Na Fase 10, apenas
  `fake-vision` é executável.
- `privacy.vision.local_only`: documenta que o provider padrão é local.

Quando o arquivo está ausente, o bootstrap usa os mesmos defaults seguros do
arquivo versionado.
