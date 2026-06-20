# Startup Launcher e Experiência de Inicialização

## Objetivo

O `private-ai-companion` deve ser amigável para usuários finais. O usuário comum não deve precisar abrir terminal, conhecer `uv`, ativar ambiente virtual ou digitar comandos para iniciar a aplicação.

O projeto deve fornecer um entrypoint de uso simples, especialmente no Windows, através de um `Start.bat` robusto. Comandos técnicos continuam permitidos para desenvolvedores, diagnóstico, automação e CI, mas não devem ser o fluxo principal de uso.

## Regra de produto

A experiência padrão deve ser:

```text
baixar/clonar projeto ou release
→ executar Start.bat
→ launcher valida ambiente
→ dependências são preparadas quando necessário
→ aplicação inicia com Rich + Pyfiglet exibindo private-ai-companion
→ usuário interage sem precisar digitar comandos técnicos
```

## Responsabilidades do `Start.bat`

O `Start.bat` deve ser tratado como um launcher de bootstrap, não como local de regra de negócio.

Ele deve:

- iniciar a aplicação de forma amigável no Windows;
- exibir mensagens claras para usuário final;
- detectar Python compatível quando necessário;
- preferir Python 3.12+;
- verificar se `uv` está disponível ou orientar instalação de forma clara;
- preparar/criar ambiente local do projeto quando necessário;
- sincronizar dependências usando o fluxo oficial do projeto;
- iniciar o entrypoint Python oficial;
- redirecionar logs para local adequado;
- não conter lógica de produto;
- não conter segredos;
- não executar comandos destrutivos;
- falhar com mensagem compreensível e código de saída adequado.

## Estado na Fase 01

O `Start.bat` inicial já existe e executa o fluxo mínimo:

```text
Start.bat
→ valida presença de uv
→ valida Python 3.12 pelo Windows py launcher
→ chama uv run private-ai-companion
→ entrypoint definido em pyproject.toml
```

Na Fase 03, o entrypoint monta a aplicação pelo bootstrap e inicia a CLI com
Rich/Pyfiglet. O usuário vê o banner `private-ai-companion` ao iniciar pelo
`Start.bat` e pode conversar por texto usando a resposta local temporária da
fase.

Na Fase 04, o launcher também pode repassar `--persona-config` para o entrypoint
oficial. A leitura e validação do arquivo continuam no bootstrap Python, não no
`Start.bat`.

Na Fase 05, o launcher também pode repassar `--providers-config`. A seleção de
providers e o roteamento de LLM continuam no bootstrap Python e no módulo
`brain/`; o `Start.bat` não contém lógica de provider.

Na Fase 07, o launcher também pode repassar `--speech-config`. A configuração de
TTS, fila e playback continua no bootstrap Python e no módulo `speech/`; o
`Start.bat` não contém lógica de áudio.

Na Fase 08, o launcher também pode repassar `--voice-file` para validar entrada
por voz a partir de um arquivo explícito. A transcrição, VAD e seleção de STT
continuam no bootstrap Python, `interaction/` e `speech/`; o `Start.bat` não
captura microfone nem chama `faster-whisper` diretamente.

Na Fase 09, o launcher também pode repassar `--avatar-config` e
`--avatar-expression`. Configuração, provider fake, VTube Studio, hotkeys e
lipsync continuam no bootstrap Python, `avatar/` e `adapters/avatar/`; o
`Start.bat` não contém lógica de avatar nem token do VTube Studio.

Na Fase 10, o launcher também pode repassar `--privacy-config`,
`--screen-context` e `--screen-purpose`. Policy de privacidade, seleção de
provider fake/local, redaction e contexto visual temporário continuam no
bootstrap Python, `vision/` e `adapters/vision/`; o `Start.bat` não captura tela,
não persiste screenshot e não envia imagem para API externa.

Na Fase 11, o launcher também pode repassar `--desktop-config`,
`--desktop-action`, `--desktop-dry-run` e `--desktop-confirm`. Classificação de
risco, policy, permissões, dry-run, confirmação e audit log continuam no
bootstrap Python, `safety/`, `desktop/` e `adapters/desktop/`; o `Start.bat` não
contém lógica de ação local e não executa comandos do sistema em nome da
companion.

Na Fase 12, o launcher também pode repassar `--skills-config`, `--skill`,
`--skill-input`, `--skill-dry-run` e `--skill-confirm`. Manifest, registry,
policy de skills e execução de efeitos continuam no bootstrap Python,
`skills/`, `safety/` e `desktop/`; o `Start.bat` não contém lógica de skill,
não interpreta manifests e não executa efeitos diretamente.

Na Fase 13, o launcher também pode repassar `--memory-config`, `--dashboard` e
`--tray-status`. Dashboard, modelo local de tray, leitura de configuração,
contagens de memória e permissões continuam no bootstrap Python e em `ui/`; o
`Start.bat` não renderiza painel, não lê banco SQLite e não interpreta
permissões.

Na Fase 14, o launcher também pode repassar `--observability-config` e
`--diagnostics`. Configuração de observabilidade, health checks, métricas,
replay de eventos sanitizado e logs estruturados continuam no bootstrap Python,
`observability/` e `ui/`; o `Start.bat` não lê logs, não inspeciona eventos e
não implementa regras de diagnóstico.

## Responsabilidades que não pertencem ao `Start.bat`

O `Start.bat` não deve:

- implementar lógica de conversa;
- chamar LLM, STT, TTS, avatar, memória ou skills diretamente;
- executar ações locais da companion;
- armazenar API keys;
- modificar arquivos de usuário fora do diretório do projeto sem confirmação;
- instalar programas de sistema silenciosamente;
- ignorar falhas de validação;
- virar substituto do bootstrap Python.

## Relação com a arquitetura

A arquitetura deve manter esta separação:

```text
Start.bat
→ scripts/start.ps1 ou comando equivalente, se necessário
→ python -m private_ai_companion
→ bootstrap/app_factory
→ core/runtime
→ módulos/adapters
```

O `Start.bat` é uma porta de entrada operacional. O núcleo do sistema continua dentro de `src/private_ai_companion/`.

## UX mínima esperada

Ao iniciar, o usuário deve ver:

- banner com Pyfiglet mostrando `private-ai-companion`;
- status de carregamento;
- ambiente detectado;
- modo atual de execução;
- avisos de configuração ausente, quando houver;
- instrução simples para configurar `.env` quando necessário;
- mensagem clara se algum provedor opcional não estiver configurado;
- estado inicial da companion.

## Fluxos suportados

### Usuário final Windows

```text
Start.bat
→ valida ambiente
→ inicia aplicação
```

### Desenvolvedor

```text
uv run private-ai-companion
```

ou comando equivalente definido pelo Codex durante a implementação.

### Diagnóstico

```text
Start.bat --diagnostics
```

ou alternativa equivalente documentada, desde que preserve simplicidade para usuário final.

## Critérios de qualidade

O launcher deve ser testado/validado para:

- ambiente sem `.env`;
- ambiente com `.env` incompleto;
- Python ausente ou incompatível;
- `uv` ausente;
- dependências não sincronizadas;
- execução normal;
- falha de startup;
- logs gravados corretamente.

## Critério de conclusão

O projeto não deve ser considerado pronto para release enquanto um usuário Windows não conseguir iniciar a aplicação por um caminho simples e documentado, preferencialmente `Start.bat`, sem precisar conhecer comandos técnicos.
