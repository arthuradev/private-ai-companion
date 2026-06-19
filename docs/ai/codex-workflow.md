# Codex Workflow

## Objetivo

Definir como o Codex deve implementar `private-ai-companion` sem depender de prompts gigantes colados no chat.

## Fluxo oficial

1. Ler `AGENTS.md`.
2. Ler `SDD.md`.
3. Ler `ARCHITECTURE.md`.
4. Ler `GSD.md`.
5. Ler `SECURITY.md`.
6. Ler `CONTRIBUTING.md`.
7. Ler `docs/architecture/overview.md`.
8. Ler `docs/architecture/module-boundaries.md`.
9. Ler documentos em `docs/implementation/` em ordem numérica até a fase atual.
10. Criar branch apropriada.
11. Implementar a fase.
12. Executar validações.
13. Fazer commits.
14. Apresentar relatório.
15. Parar e pedir autorização para próxima fase.

## Autonomia permitida

O Codex pode agir sem pedir confirmação para ações operacionais comuns dentro da fase. Isso inclui commits, ajustes técnicos, criação de arquivos e correções necessárias.

## Parada obrigatória

O Codex deve parar ao final de cada fase. A parada por fase é o mecanismo de governança humana do projeto.

## Estilo de implementação

- Incremental.
- Testável.
- Documentado.
- Sem atalhos perigosos.
- Sem acoplamento desnecessário.
- Sem personalização para um usuário específico.

## Proibições

- Pular fase.
- Esconder falhas.
- Fazer alterações fora do escopo sem justificar.
- Ignorar decisões arquiteturais.
- Colocar segredos no repositório.
- Implementar automação local sem safety policy.
