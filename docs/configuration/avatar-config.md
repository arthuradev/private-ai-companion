# avatar-config

## Responsabilidade

Configuração de avatar, provider visual, expressões, hotkeys, lipsync e idle behavior.

## Arquivo padrão

```text
configs/avatar.default.toml
```

O arquivo é seguro para Git e não contém token real. O provider padrão é
`fake-avatar`, local e determinístico.

## Campos atuais

- `avatar.provider_id`: provider ativo. Valores atuais: `fake-avatar` e
  `vtube-studio`.
- `avatar.enabled`: habilita ou desabilita o serviço de avatar.
- `avatar.vtube_studio.host`: host local do servidor WebSocket do VTube Studio.
- `avatar.vtube_studio.port`: porta do Plugin API, por padrão `8001`.
- `avatar.vtube_studio.plugin_name`: nome exibido na autorização do plugin.
- `avatar.vtube_studio.plugin_developer`: desenvolvedor exibido na autorização.
- `avatar.vtube_studio.authentication_token_env`: variável de ambiente que guarda
  o token local.
- `avatar.vtube_studio.request_token_on_connect`: quando `true`, solicita token ao
  VTube Studio se não houver token no ambiente.
- `avatar.expression_hotkeys`: mapa de expressão para hotkey ID/nome do VTube
  Studio.
- `avatar.idle.enabled`: habilita estado idle planejado.
- `avatar.idle.expression`: expressão de idle.
- `avatar.idle.interval_seconds`: intervalo planejado de idle.
- `avatar.lipsync.enabled`: habilita lipsync planejado.
- `avatar.lipsync.parameter_name`: parâmetro VTube Studio para boca.
- `avatar.lipsync.weight`: peso de injeção do parâmetro, de `0` a `1`.

## VTube Studio

Para usar VTube Studio:

1. Instale o extra opcional com `uv sync --extra avatar`.
2. Ative Plugin API access no VTube Studio.
3. Configure `avatar.provider_id = "vtube-studio"`.
4. Configure hotkeys em `avatar.expression_hotkeys`.
5. Mantenha o token real apenas em `.env`, por exemplo
   `PRIVATE_AI_COMPANION_VTS_TOKEN=...`.

Não coloque tokens em `configs/avatar.default.toml`.

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
