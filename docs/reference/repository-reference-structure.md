# Estrutura de Repositório de Referência

Este documento mostra a estrutura que o Codex deve criar quando implementar código.

```text
Start.bat
configs/
assets/
data/
scripts/
src/private_ai_companion/
tests/
docs/
```

## Observação

A partir da Fase 01, a estrutura Python inicial já existe com `pyproject.toml`,
`src/private_ai_companion/`, `tests/`, `configs/`, `assets/`, `scripts/` e
`Start.bat`.

Diretórios de dados privados continuam fora do Git por padrão. O diretório
`data/` deve ser criado em tempo de execução ou por instrução explícita quando
houver necessidade real.

## Launcher

A estrutura real inclui `Start.bat` na raiz do repositório como launcher
Windows inicial. Ele chama o entrypoint oficial definido em `pyproject.toml` e
não contém regra de negócio.
