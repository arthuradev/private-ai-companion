# Módulo `brain`

## Responsabilidade

Contém persona, prompt builder, context builder, LLM router, response planner e emotion planner. Não executa ações locais.

## Implementado na Fase 04

- Modelo tipado de persona.
- Persona padrão segura e configurável.
- Context builder para mensagens de texto.
- Prompt builder estruturado com mensagens `system` e `user`.
- Marcação no prompt de que conteúdo do usuário é dado não confiável.

LLM router, response planner e emotion planner continuam para fases futuras.

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
