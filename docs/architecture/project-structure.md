# Estrutura de Projeto Planejada

Este documento descreve a estrutura que o Codex deve criar durante a implementação. A estrutura abaixo é referência; ela deve ser implementada por fases.

```text
private-ai-companion/
├── Start.bat
├── pyproject.toml
├── README.md
├── AGENTS.md
├── SDD.md
├── GSD.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE.md
├── configs/
├── assets/
├── data/
├── scripts/
├── src/
│   └── private_ai_companion/
│       ├── bootstrap/
│       ├── core/
│       ├── interaction/
│       ├── brain/
│       ├── memory/
│       ├── speech/
│       ├── avatar/
│       ├── vision/
│       ├── desktop/
│       ├── safety/
│       ├── skills/
│       ├── ui/
│       ├── config/
│       └── observability/
└── tests/
    ├── unit/
    ├── integration/
    ├── contract/
    ├── security/
    ├── architecture/
    └── e2e/
```

## Regras

- `data/` não deve ser versionado, exceto placeholders necessários.
- `.env` real não deve ser versionado.
- Configurações versionáveis ficam em `configs/`.
- Dados privados ficam em `data/`.
- Código fica em `src/`.
- Testes ficam em `tests/`.

## Entry point amigável

A estrutura real de código deve incluir `Start.bat` na raiz do repositório como entrypoint amigável para usuários Windows.

O arquivo existe para UX e bootstrap. Ele não deve conter lógica de produto. O fluxo interno deve continuar em `src/private_ai_companion/`.

Além disso, a estrutura pode incluir scripts auxiliares em `scripts/`, desde que o `Start.bat` permaneça simples, seguro e compreensível.
