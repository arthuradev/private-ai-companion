# Política de Segredos

## Regras

- `.env` real não entra no Git.
- API keys devem ser mascaradas em logs.
- Configuração versionável não deve conter segredo.
- O projeto deve fornecer `.env.example` quando o código for implementado.
- SecretsGuard deve detectar padrões comuns de chaves.

## Exemplos de segredo

- API keys.
- Tokens de OAuth.
- Tokens locais de plugin, como `PRIVATE_AI_COMPANION_VTS_TOKEN`.
- Senhas.
- Chaves privadas.
- URLs com credenciais.
