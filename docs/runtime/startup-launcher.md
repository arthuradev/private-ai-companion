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

O `Start.bat` futuro deve ser tratado como um launcher de bootstrap, não como local de regra de negócio.

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
