# providers-config

## Responsabilidade

Configuração de providers LLM/STT/TTS/vision, incluindo prioridade, fallback e modo local/cloud.

## Arquivo padrão

A Fase 05 adiciona:

```text
configs/providers.default.toml
```

O arquivo é seguro para Git e não contém segredos. Ele habilita apenas o provider
fake local:

```text
fake-local
```

Providers locais/cloud planejados aparecem desabilitados por padrão. Campos como
`api_key_env` indicam o nome esperado da variável de ambiente, não o valor do
segredo.

## Campos atuais de LLM

- `default_provider`: provider usado primeiro pelo router.
- `fallback_order`: ordem de fallback.
- `providers[].id`: identificador estável do provider.
- `providers[].kind`: `fake`, `local` ou `cloud`.
- `providers[].model`: nome do modelo planejado/configurado.
- `providers[].enabled`: habilita ou desabilita o provider.
- `providers[].requires_api_key`: informa se depende de segredo.
- `providers[].api_key_env`: nome da variável de ambiente esperada.

## Estado na Fase 05

Somente providers `fake` são executáveis. Providers `local` e `cloud` estão
documentados/configuráveis, mas ainda não possuem adapter de execução real.

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
