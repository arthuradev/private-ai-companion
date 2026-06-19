# CONTRIBUTING.md

Obrigado por considerar contribuir com `private-ai-companion`.

## 1. Filosofia de contribuição

Contribuições devem preservar:

- privacidade;
- segurança;
- modularidade;
- testabilidade;
- clareza arquitetural;
- personalização pelo usuário;
- ausência de acoplamento com plataformas de live.

## 2. Antes de contribuir

Leia:

1. `README.md`
2. `ARCHITECTURE.md`
3. `SECURITY.md`
4. `GSD.md`
5. `docs/architecture/module-boundaries.md`
6. `docs/workflows/testing-strategy.md`

## 3. Branches

Use nomes claros:

```text
phase/01-foundation
feat/tts-queue
fix/memory-policy-redaction
docs/security-policy
refactor/event-bus-boundaries
```

## 4. Commits

Use Conventional Commits:

```text
feat(memory): add memory candidate policy
fix(safety): block critical desktop actions
docs(architecture): explain avatar adapter boundary
test(skills): cover manifest validation
```

## 5. Pull requests

Cada PR deve:

- ter escopo claro;
- explicar motivação;
- listar validações;
- atualizar documentação se necessário;
- incluir testes;
- não misturar mudanças independentes.

## 6. Regras técnicas

- Não adicionar provider externo sem adapter.
- Não adicionar skill sem manifest e permissões.
- Não adicionar ação local sem policy.
- Não salvar dados privados por padrão.
- Não quebrar `core/` com dependências externas.

## 7. Validações esperadas

Quando houver código:

```text
ruff format --check
ruff check
pytest
pyright
```

Também devem existir testes de arquitetura e segurança quando a mudança tocar boundaries, actions, memory, vision ou desktop.

## 8. Decisões arquiteturais

Mudanças significativas devem criar ou atualizar ADR em `docs/architecture/adr/`.

Não reescreva ADRs aceitas para esconder histórico. Se uma decisão mudou, crie nova ADR substituindo a anterior.
