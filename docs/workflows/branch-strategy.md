# Estratégia de Branches

## Modelo

Usar modelo misto:

- `main`: branch principal estável.
- `phase/XX-name`: fases grandes de implementação.
- `feat/name`: features isoladas.
- `fix/name`: correções.
- `docs/name`: documentação.

## Regras

- Branches de fase podem conter múltiplos commits.
- Não misturar fases diferentes na mesma branch.
- `main` deve permanecer funcional.
- Commits devem ser claros e pequenos.
