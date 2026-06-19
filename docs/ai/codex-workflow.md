# Codex Workflow

## Objetivo

Definir como o Codex deve implementar `private-ai-companion` sem depender de prompts gigantes colados no chat.

## Fluxo oficial

1. Ler `PROMPT-CODEX.md`.
2. Ler `AGENTS.md`.
3. Ler `SDD.md`.
4. Ler `ARCHITECTURE.md`.
5. Ler `GSD.md`.
6. Ler documento da fase atual.
7. Criar branch apropriada.
8. Implementar a fase.
9. Executar validações.
10. Fazer commits.
11. Apresentar relatório.
12. Parar e pedir autorização para próxima fase.

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
