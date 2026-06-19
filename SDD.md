# SDD.md — Software Design Document

## 1. Identidade do projeto

Nome: `private-ai-companion`

Tipo: aplicação desktop open-source para companheira virtual privada.

Linguagem principal planejada: Python 3.12+.

Público-alvo:

- usuários que desejam uma presença virtual privada no desktop;
- desenvolvedores que desejam estudar ou adaptar uma arquitetura de companion AI;
- pessoas interessadas em LLMs, voz, avatar, memória local e interação segura;
- contribuidores open-source.

## 2. Problema

Modelos de IA conseguem conversar e gerar código, mas sistemas de companheira virtual frequentemente nascem como protótipos improvisados: um script principal enorme, pouca separação de responsabilidade, memória frágil, segurança superficial, avatar acoplado ao fluxo de conversa e automação local perigosa.

Este projeto existe para criar uma base séria, modular e segura para uma companheira virtual privada de desktop.

## 3. Objetivo central

Criar uma companheira virtual privada para desktop, com personalidade, voz, avatar, memória local e interação segura.

## 4. O que o projeto é

O projeto é:

- uma aplicação desktop local-first;
- uma base open-source personalizável;
- uma companheira virtual privada;
- um sistema modular com voz, avatar, memória e skills;
- uma arquitetura preparada para LLMs locais e cloud;
- uma plataforma segura para interação limitada com desktop.

## 5. O que o projeto não é

O projeto não é:

- streamer virtual;
- bot de Twitch;
- bot de YouTube;
- integração de OBS;
- bot para audiência pública;
- assistente corporativo genérico;
- automação irrestrita do sistema operacional;
- ferramenta para executar comandos gerados livremente por LLM.

## 6. Requisitos funcionais

### RF-001 — Conversa por texto

O sistema deve permitir conversa por texto entre usuário e personagem.

### RF-002 — Persona configurável

O sistema deve permitir configurar nome, estilo de fala, tom, limites e comportamento da personagem sem alterar código.

### RF-003 — LLM router híbrido

O sistema deve suportar provedores locais e cloud por meio de adapters substituíveis.

### RF-004 — Voz de saída

O sistema deve converter respostas em voz usando adapters de TTS.

### RF-005 — Interrupção de fala

O sistema deve permitir cancelar/interromper a fila de fala quando o usuário interagir novamente.

### RF-006 — Entrada por voz

O sistema deve transcrever fala do usuário, inicialmente com STT local usando `faster-whisper`.

### RF-007 — Avatar visual

O sistema deve controlar um avatar visual por meio de adapter, inicialmente com VTube Studio + Live2D.

### RF-008 — Expressões e presença

O sistema deve mapear estados emocionais e interacionais para expressões, idle behavior e lipsync.

### RF-009 — Memória local

O sistema deve manter memória local em SQLite, com política de retenção, aprovação, edição e exclusão.

### RF-010 — Visão de tela autorizada

O sistema deve permitir contexto visual de tela/janela ativa apenas com permissão e política de privacidade.

### RF-011 — Ações locais seguras

O sistema deve permitir ações locais de baixo/médio risco, como mudar avatar, criar notas, abrir apps permitidos e ler título de janela, sempre com política de segurança.

### RF-012 — Skills/plugins

O sistema deve permitir skills registradas, testáveis e governadas por permissões.

### RF-013 — UI inicial

O sistema deve iniciar com interface em terminal usando Rich e Pyfiglet, exibindo o nome do projeto de forma clara e amigável.

### RF-014 — Dashboard/tray futuro

O sistema deve incluir UI complementar para status, memória, permissões e configuração.

### RF-015 — Inicialização amigável por launcher

O sistema deve fornecer um fluxo de inicialização amigável para usuário final no Windows, preferencialmente por `Start.bat`, sem exigir que o usuário comum digite comandos técnicos. O launcher deve validar ambiente, preparar dependências quando necessário e iniciar o entrypoint oficial da aplicação sem conter regra de negócio.

## 7. Requisitos não funcionais

### Segurança

Ações locais devem ser governadas. O LLM nunca executa comandos diretamente.

### Privacidade

Dados privados devem permanecer locais por padrão. Envio a APIs externas deve ser explícito, configurável e auditável.

### Modularidade

LLM, STT, TTS, avatar, memória, visão, desktop e UI devem ser substituíveis.

### Testabilidade

Módulos críticos devem ser testáveis com providers fake e adapters simulados.

### Observabilidade

O sistema deve ter logs estruturados, health checks, métricas de latência e replay de eventos.

### Manutenibilidade

O projeto deve evitar arquivos centrais gigantes, dependências cíclicas e responsabilidades misturadas.

### Personalização

A personalidade padrão deve ser carinhosa/próxima, mas claramente substituível pelo usuário.

## 8. Escopo completo planejado

O projeto deve chegar a um sistema funcional com:

- estrutura Python completa;
- event bus interno;
- conversa por texto;
- prompt builder;
- LLM router;
- memória SQLite;
- TTS;
- STT;
- avatar VTube Studio/Live2D;
- visão de tela autorizada;
- ações locais seguras;
- skills/plugins;
- UI com Rich/Pyfiglet;
- dashboard/tray;
- logs e diagnóstico;
- empacotamento/release;
- documentação viva.

## 9. Fora do escopo

- Twitch;
- YouTube;
- OBS como requisito central;
- live streaming;
- chat público;
- automação irrestrita de mouse/teclado;
- execução de shell livre gerada por LLM;
- captura contínua de tela por padrão;
- coleta oculta de dados;
- personalidade fixa obrigatória.

## 10. Critérios de aceitação final

O projeto será considerado completo quando:

- todas as fases em `docs/implementation/` estiverem concluídas;
- conversa por texto funcionar;
- voz de entrada e saída funcionar;
- avatar responder a estados da conversa;
- memória local estiver funcional e editável;
- visão de tela funcionar com permissão;
- ações locais permitidas estiverem governadas por policy;
- skills puderem ser registradas e testadas;
- UI inicial e painel complementar estiverem disponíveis;
- testes, lint e typecheck passarem;
- documentação refletir o código real;
- release/tag SemVer estiver criada;
- o projeto puder ser usado por terceiros sem caminhos ou configurações pessoais.

### Usabilidade de inicialização

O projeto deve priorizar um fluxo de uso amigável. Comandos técnicos podem existir para desenvolvimento e diagnóstico, mas a experiência padrão no Windows deve permitir iniciar a aplicação por `Start.bat` ou launcher equivalente. O usuário não deve precisar saber ativar ambiente virtual, chamar `uv`, rodar módulo Python ou lembrar comandos internos.
