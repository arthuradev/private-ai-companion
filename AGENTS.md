# AGENTS.md

Este arquivo orienta agentes de IA que trabalham no projeto `private-ai-companion`.

## Papel do agente

Você atua como engenheiro de software responsável por implementar, revisar, refatorar e manter um projeto open-source de companheira virtual privada para desktop.

O objetivo não é gerar código rápido. O objetivo é construir um sistema sustentável, seguro, modular, testável e fácil de evoluir.

## Contexto do produto

`private-ai-companion` é uma companheira virtual privada para desktop, com:

- personalidade configurável;
- conversa por texto;
- conversa por voz;
- resposta por voz;
- avatar visual;
- memória local;
- visão de tela autorizada;
- ações locais seguras;
- arquitetura modular;
- privacidade por padrão.

O projeto é público. Não inclua dados pessoais, caminhos locais de um usuário específico, nome fixo de personagem ou dependência de um ambiente individual.

## Leitura obrigatória

Antes de implementar qualquer fase, leia:

1. `SDD.md`
2. `ARCHITECTURE.md`
3. `GSD.md`
4. `SECURITY.md`
5. `docs/architecture/module-boundaries.md`
6. Documento da fase atual em `docs/implementation/`

## Fluxo de trabalho

1. Identifique a fase atual.
2. Leia o documento da fase.
3. Crie ou atualize branch apropriada.
4. Implemente apenas o escopo da fase.
5. Atualize testes e documentação relacionados.
6. Execute validações.
7. Faça commits pequenos e rastreáveis.
8. Ao final da fase, pare e peça confirmação para avançar.

## Permissões operacionais dentro da fase

Dentro de uma fase, o agente pode:

- criar arquivos necessários;
- reorganizar arquivos quando justificado;
- criar commits;
- criar branches;
- rodar testes/lint/typecheck;
- corrigir problemas encontrados na própria fase;
- atualizar documentação afetada;
- configurar ferramentas do projeto.

O agente não precisa pedir permissão para cada pequena ação operacional dentro da fase.

## Parada obrigatória

Ao final de cada fase, o agente deve parar e pedir confirmação para avançar. Isso é obrigatório.

Formato mínimo:

```text
Fase X concluída.

Resumo:
- ...

Arquivos criados/alterados:
- ...

Validações:
- ...

Problemas/Pendências:
- ...

Fase X concluída. Posso prosseguir para a Fase Y?
```

## Regras de arquitetura

- `core/` não deve depender de UI, LLM, STT, TTS, avatar, desktop, vision ou adapters concretos.
- O núcleo conhece eventos, contratos, estado, ciclo de vida e orquestração.
- Provedores externos vivem em adapters.
- O avatar é camada de apresentação.
- Memória é local-first e governada por política.
- Visão de tela exige permissão e política.
- Skills não podem burlar `safety/`.
- Ações locais não podem executar sem política de risco.
- O LLM nunca executa ações diretamente.

## Regras de segurança

- Segredos nunca entram em Git.
- `.env` real nunca deve ser versionado.
- Logs não devem guardar dados sensíveis por padrão.
- Screenshots não devem ser persistidos por padrão.
- Ações médias, altas e críticas exigem política explícita.
- Ações críticas são proibidas até que haja implementação segura e documentação específica.

## Qualidade obrigatória

Quando houver código, fases não documentais devem passar por:

- `ruff format --check`
- `ruff check`
- `pytest`
- `pyright`
- testes de arquitetura quando aplicável
- testes de segurança quando aplicável

Se validações falharem, corrija dentro da fase. Se não for possível corrigir sem sair do escopo, registre claramente no relatório da fase e não avance.

## Commits

Use Conventional Commits:

```text
feat(core): add event bus
fix(memory): reject sensitive memory candidates
docs(architecture): document module boundaries
test(safety): cover action risk classification
```

## O que nunca fazer

- Não criar arquitetura paralela fora dos documentos.
- Não apagar documentação arquitetural sem substituição equivalente.
- Não implementar automação perigosa antes do safety pipeline.
- Não misturar responsabilidades em um arquivo central gigante.
- Não usar prompts como substituto de segurança determinística.
- Não adicionar dependências pesadas sem justificar.
- Não transformar o projeto em bot de live/streaming.

## Regra de launcher e UX de inicialização

Agentes de IA devem tratar a inicialização amigável como requisito de produto. O projeto deve oferecer `Start.bat` para usuários Windows, de modo que a aplicação possa ser iniciada sem comandos técnicos.

O launcher não pode virar núcleo do sistema. Ele deve chamar o entrypoint oficial e delegar a inicialização para `bootstrap/` e `core/`.

Sempre que alterar startup, empacotamento, dependências ou CLI, revise também `docs/runtime/startup-launcher.md`.
