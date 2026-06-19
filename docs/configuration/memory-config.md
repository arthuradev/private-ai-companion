# memory-config

## Responsabilidade

Configuração de SQLite, retenção, aprovação automática, sensibilidade, sumarização e edição.

## Arquivo padrão

A Fase 06 adiciona:

```text
configs/memory.default.toml
```

O arquivo é seguro para Git e não contém dados privados. O caminho padrão aponta
para:

```text
data/memory.sqlite3
```

O diretório `data/` continua ignorado pelo Git e deve conter apenas dados locais
do usuário.

## Campos atuais

- `database_path`: caminho do SQLite local.
- `auto_approve_low_sensitivity`: se memórias de baixa sensibilidade podem ser
  aprovadas automaticamente.
- `retention_days`: retenção planejada em dias.
- `policy.reject_sensitive_by_default`: rejeita conteúdo sensível por padrão.
- `policy.minimum_confidence`: confiança mínima para aceitar candidata.

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
