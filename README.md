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

Este repositório já possui a base implementada até a Fase 14:

- projeto Python 3.12+ com `src/`;
- `uv`, `ruff`, `pytest` e `pyright` configurados;
- pacote `private_ai_companion`;
- entrypoint oficial `private-ai-companion`;
- runtime central com event bus, lifecycle, orquestrador e estado;
- CLI inicial com Rich/Pyfiglet e conversa por texto local;
- persona configurável por TOML;
- context builder e prompt builder testáveis;
- LLM router com provider fake local e providers locais/cloud planejados;
- memória local SQLite com policy e revisão explícita;
- TTS fake local, fila de fala, audio player fake e interrupção testável;
- STT fake local, VAD simples, entrada por voz a partir de clipe explícito e
  adapter opt-in para `faster-whisper`;
- avatar service com estados visuais, expressões, idle, lipsync, provider fake
  e adapter opt-in para VTube Studio;
- vision service com captura manual autorizada, redaction de metadados de texto,
  provider fake/local e eventos sensíveis sem bytes de screenshot;
- safety pipeline para ações locais com classificação de risco, policy,
  dry-run, confirmação, audit log em memória e eventos sem parâmetros sensíveis;
- desktop action service com leitura simulada de título de janela, notas locais
  em diretório permitido e abertura simulada de apps allowlisted;
- sistema inicial de skills com manifest, registry, manager governado por
  policy e eventos sanitizados;
- skills embutidas `builtin.status`, `builtin.local_note` e
  `builtin.open_allowed_app`;
- dashboard local em Rich para status, configuração, memória e permissões;
- modelo local de tray/status com menu testável e sem dependência nativa pesada;
- observabilidade local com logs estruturados em memória, métricas de eventos,
  replay sanitizado e health checks;
- `Start.bat` inicial para usuários Windows;
- testes de sanidade, runtime, interação por texto/voz, prompt, LLM router,
  memória, speech, avatar, visão, desktop, skills, dashboard/tray, safety,
  observabilidade, config, CLI, segurança e boundaries arquiteturais.

Ordem de leitura recomendada:

1. `AGENTS.md`
2. `SDD.md`
3. `ARCHITECTURE.md`
4. `GSD.md`
5. `SECURITY.md`
6. `docs/implementation/`

## Stack planejada

- Python 3.12+
- `uv` para gerenciamento de projeto/dependências
- `ruff` para lint e formatação
- `pytest` para testes
- `pyright` para type checking
- `pydantic` para validação de configurações, eventos e schemas
- SQLite para memória local
- Rich + Pyfiglet para CLI inicial
- Rich para dashboard/tray local inicial
- logs estruturados, métricas e replay em memória por padrão
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

Configuração padrão de memória local:

```text
configs/memory.default.toml
```

A Fase 06 implementa repository SQLite, policy e revisão de memórias. A conversa
ainda não grava memórias automaticamente.

Para usar um arquivo de memória específico:

```text
uv run private-ai-companion --memory-config configs/memory.default.toml
```

Configuração padrão de fala:

```text
configs/speech.default.toml
```

A Fase 07 implementa TTS fake local, fila de fala e interrupção. A conversa
ainda não reproduz áudio real automaticamente.

A Fase 08 implementa entrada por voz a partir de um clipe explícito, VAD simples,
STT fake local e adapter `faster-whisper` opt-in. O microfone real permanece
desabilitado por padrão e não há captura contínua de áudio.

Para validar o fluxo de voz fake com um arquivo de texto usado como transcrição:

```text
uv run private-ai-companion --voice-file caminho/para/voice.txt
```

Para usar `faster-whisper`, instale o extra opcional e altere
`speech.stt.provider_id` para `faster-whisper` em `configs/speech.default.toml`
ou em um arquivo de configuração próprio:

```text
uv sync --extra stt
```

Configuração padrão de avatar:

```text
configs/avatar.default.toml
```

A Fase 09 implementa provider fake local, estados visuais e adapter VTube Studio
opt-in. Por padrão, VTube Studio não é chamado. Para validar uma expressão fake:

```text
uv run private-ai-companion --avatar-expression happy
```

Para usar VTube Studio, instale o extra opcional, altere
`avatar.provider_id` para `vtube-studio`, configure hotkeys em
`avatar.expression_hotkeys` e mantenha o token local em `.env` usando
`PRIVATE_AI_COMPANION_VTS_TOKEN`:

```text
uv sync --extra avatar
```

Configuração padrão de privacidade e visão:

```text
configs/privacy.default.toml
```

A Fase 10 implementa o fluxo de contexto visual temporário com policy
determinística. Por padrão, a captura exige autorização humana, não persiste
screenshot, não permite captura contínua e não envia imagem para API externa.
O provider padrão é fake/local para desenvolvimento e testes.

Para validar o fluxo de contexto de tela pelo entrypoint oficial:

```text
uv run private-ai-companion --screen-context
```

No Windows, o launcher continua apenas delegando para o entrypoint Python:

```text
Start.bat --screen-context
```

Configuração padrão de ações locais seguras:

```text
configs/desktop.default.toml
```

A Fase 11 implementa o primeiro pipeline de ações locais. Ações médias exigem
confirmação por padrão, ações críticas são bloqueadas, e o LLM não executa
comandos diretamente. O executor padrão não roda shell nem automação livre de
mouse/teclado.

Para validar uma ação em dry-run:

```text
uv run private-ai-companion --desktop-action open-allowed-app --app-id calculator --desktop-dry-run
```

Para executar uma ação média confirmada pelo usuário:

```text
uv run private-ai-companion --desktop-action read-active-window-title --desktop-confirm
```

No Windows, o launcher continua delegando:

```text
Start.bat --desktop-action read-active-window-title --desktop-confirm
```

Configuração padrão de skills:

```text
configs/skills.default.toml
```

A Fase 12 implementa manifests, registry e manager de skills. Skills podem
declarar permissões e efeitos, mas efeitos locais continuam passando pelo
pipeline de ações seguras. O LLM não executa comandos diretamente, e skills não
podem burlar `safety/`.

Para validar uma skill sem efeito local:

```text
uv run private-ai-companion --skill builtin.status
```

Para validar uma skill que solicita a abertura de app permitido em dry-run:

```text
uv run private-ai-companion --skill builtin.open_allowed_app --skill-input app_id=calculator --skill-dry-run
```

No Windows, o launcher continua delegando ao entrypoint oficial:

```text
Start.bat --skill builtin.status
```

UI complementar local:

```text
uv run private-ai-companion --dashboard
uv run private-ai-companion --tray-status
```

A Fase 13 implementa um dashboard local em Rich com status de runtime,
configuração, contagens de memória, permissões de desktop e skills habilitadas.
O modo `--tray-status` expõe o primeiro modelo de tray/menu em formato local e
testável. Integração nativa com bandeja do sistema pode evoluir depois sem
colocar regra de negócio na UI.

No Windows, o launcher continua delegando:

```text
Start.bat --dashboard
Start.bat --tray-status
```

Configuração padrão de observabilidade:

```text
configs/observability.default.toml
```

A Fase 14 implementa logs estruturados em memória, métricas de eventos, replay
sanitizado e health checks. Payloads privados, como texto do usuário e resposta
gerada, são redigidos por padrão.

Para validar diagnóstico local:

```text
uv run private-ai-companion --diagnostics
```

No Windows, o launcher continua delegando:

```text
Start.bat --diagnostics
```

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
