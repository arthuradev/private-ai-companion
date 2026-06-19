# Política de Captura de Tela

## Regras

- Captura contínua é proibida por padrão.
- Captura deve ser solicitada ou autorizada.
- Usuário deve saber quando screenshot é criado.
- Screenshot não deve ser salvo por padrão.
- Envio para API externa depende de configuração e confirmação.
- Redaction deve ser aplicada quando possível.
- Eventos de visão não devem carregar bytes de screenshot nem texto visual cru.

## Estado na Fase 10

A policy implementada em `ScreenCapturePolicy` bloqueia por padrão:

- captura quando `user_authorized` é falso;
- modo `continuous`;
- persistência de screenshot;
- análise externa.

O comando `--screen-context` representa uma solicitação manual e explícita no
CLI. O provider default é fake/local, portanto a Fase 10 valida o pipeline de
privacidade sem observar a tela real do usuário.

## Fluxo

```text
Request
→ Policy check
→ Explicit user authorization
→ One-shot capture provider
→ Redaction
→ Local/fake vision analysis
→ Temporary context
→ Discard or explicit save
```
