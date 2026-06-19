# Política de Captura de Tela

## Regras

- Captura contínua é proibida por padrão.
- Captura deve ser solicitada ou autorizada.
- Usuário deve saber quando screenshot é criado.
- Screenshot não deve ser salvo por padrão.
- Envio para API externa depende de configuração e confirmação.
- Redaction deve ser aplicada quando possível.

## Fluxo

```text
Request
→ Policy check
→ Permission
→ Capture
→ Redaction
→ Vision analysis
→ Temporary context
→ Discard or explicit save
```
