# Módulo `core`

## Responsabilidade

Runtime central: eventos, event bus, orquestrador, lifecycle, estado, contratos e erros. Deve permanecer pequeno e desacoplado.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- Contratos de outros módulos, quando necessário.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
