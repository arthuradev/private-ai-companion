# Limites entre Módulos

## Regra de ouro

Um módulo só deve conhecer o que precisa conhecer. Dependências devem apontar para contratos, não implementações concretas.

## Regras

| Módulo | Pode depender de | Não pode depender de |
|---|---|---|
| `core` | tipos básicos, contratos | UI, providers, desktop, avatar concreto |
| `interaction` | core, brain contracts, speech/avatar contracts | providers concretos |
| `brain` | memory contracts, LLM contracts | desktop executor, avatar concreto |
| `memory` | storage abstractions, policy | UI, avatar, desktop |
| `speech` | STT/TTS contracts, audio | memory policy direta, desktop |
| `avatar` | avatar state/contracts | LLM, memory, desktop |
| `vision` | policy, vision contracts | execução automática de ações |
| `desktop` | safety, action contracts | LLM direto |
| `skills` | registry, safety, contracts | bypass de safety |
| `ui` | services públicos | regra de negócio |
| `observability` | core events, métricas, logs sanitizados | UI, adapters, providers concretos, payload privado bruto |

## Testes de arquitetura

O projeto deve incluir testes que detectem importações proibidas e dependências circulares.
