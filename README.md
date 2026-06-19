# private-ai-companion

`private-ai-companion` é um projeto open-source para construir uma companheira virtual privada para desktop, com personalidade configurável, conversa por texto, conversa por voz, resposta por voz, avatar visual, memória local, visão de tela autorizada e interação segura com o ambiente do usuário.

O projeto **não é** uma streamer virtual, não é um bot de Twitch, não é um bot de YouTube, não depende de OBS e não é desenhado para chat público. A arquitetura é orientada a uma presença privada no desktop, local-first sempre que possível, com integração a provedores de IA quando fizer sentido.

## Objetivo

Criar uma base técnica robusta para uma personagem virtual privada que possa:

- conversar por texto;
- ouvir por voz com STT;
- responder por voz com TTS;
- controlar um avatar visual;
- manter memória local auditável;
- usar personalidade configurável;
- analisar tela/janela ativa apenas com permissão;
- executar ações locais seguras através de política de risco;
- crescer por módulos, adapters e skills sem quebrar o núcleo.

## Princípios

1. **Privacidade por padrão**: dados pessoais, memória, sessões, screenshots e logs sensíveis devem permanecer locais por padrão.
2. **Personalização simples**: a personagem não tem nome fixo; identidade, estilo, voz e comportamento devem ser configuráveis.
3. **Arquitetura modular**: o núcleo não depende de LLMs, STT, TTS, avatar, desktop ou UI específicos.
4. **Avatar como apresentação**: Live2D/VTube Studio ou outra tecnologia visual representam o estado da personagem, mas não controlam a arquitetura.
5. **LLM não executa ações**: o modelo pode sugerir intenções estruturadas; políticas determinísticas decidem o que pode acontecer.
6. **Segurança antes de automação**: ações locais passam por classificação de risco, dry-run, confirmação e log quando necessário.
7. **Fases controladas**: o desenvolvimento ocorre por fases; ao final de cada fase, a IA deve parar e pedir autorização para avançar.

## Estado atual

Este repositório já possui a base implementada até a Fase 03:

- projeto Python 3.12+ com `src/`;
- `uv`, `ruff`, `pytest` e `pyright` configurados;
- pacote `private_ai_companion`;
- entrypoint oficial `private-ai-companion`;
- runtime central com event bus, lifecycle, orquestrador e estado;
- CLI inicial com Rich/Pyfiglet e conversa por texto local;
- persona configurável por TOML;
- context builder e prompt builder testáveis;
- LLM router com provider fake local e providers locais/cloud planejados;
- `Start.bat` inicial para usuários Windows;
- testes de sanidade, runtime, interação por texto, prompt, LLM router, config, CLI e boundaries arquiteturais.

Ordem de leitura recomendada:

1. `PROMPT-CODEX.md`
2. `AGENTS.md`
3. `SDD.md`
4. `ARCHITECTURE.md`
5. `GSD.md`
6. `SECURITY.md`
7. `docs/implementation/`

## Stack planejada

- Python 3.12+
- `uv` para gerenciamento de projeto/dependências
- `ruff` para lint e formatação
- `pytest` para testes
- `pyright` para type checking
- `pydantic` para validação de configurações, eventos e schemas
- SQLite para memória local
- Rich + Pyfiglet para CLI inicial
- faster-whisper para STT local
- TTS por adapters, com ênfase em ElevenLabs como opção premium
- VTube Studio + Live2D como primeiro caminho real de avatar
- LLM router híbrido com providers locais/cloud

## Como executar

### Usuário Windows

Execute:

```text
Start.bat
```

O launcher valida `uv` e Python 3.12 pelo Windows `py` launcher, então chama o
entrypoint oficial do pacote Python.

### Desenvolvimento

```text
uv sync
uv run private-ai-companion
```

Para executar uma única mensagem e encerrar, útil para validação:

```text
uv run private-ai-companion --once "olá"
```

Para usar um arquivo de persona específico:

```text
uv run private-ai-companion --persona-config configs/persona.default.toml
```

Para usar configuração explícita de providers:

```text
uv run private-ai-companion --providers-config configs/providers.default.toml
```

Por padrão, apenas o provider fake local fica habilitado. Providers locais/cloud
reais aparecem como configuração planejada desabilitada e não são chamados sem
implementação e configuração futura.

Validações atuais:

```text
uv run ruff format --check
uv run ruff check
uv run pytest
uv run pyright
```

## Documentação principal

- `SDD.md`: especificação do produto.
- `GSD.md`: guia operacional por fases.
- `ARCHITECTURE.md`: arquitetura técnica e limites entre módulos.
- `SECURITY.md`: modelo de segurança e privacidade.
- `AGENTS.md`: instruções permanentes para agentes de IA.
- `PROMPT-CODEX.md`: prompt curto para iniciar o Codex.
- `docs/architecture/`: detalhes arquiteturais.
- `docs/implementation/`: fases de implementação.
- `docs/safety/`: políticas de risco, privacidade e dados.
- `docs/modules/`: responsabilidades de cada módulo.

## Licença

Apache License 2.0. Consulte `LICENSE.md`.

## Inicialização para usuário final

O projeto mantém um fluxo amigável de inicialização no Windows. O usuário final não deve ser obrigado a conhecer comandos técnicos para abrir a companion.

Na Fase 03, o caminho recomendado já é:

```text
Start.bat
→ valida ambiente
→ prepara dependências pelo uv quando necessário
→ inicia a CLI Rich/Pyfiglet pelo entrypoint oficial private-ai-companion
```

Comandos técnicos continuam disponíveis para desenvolvedores, mantendo o `Start.bat` como entrypoint principal de uso no Windows.
