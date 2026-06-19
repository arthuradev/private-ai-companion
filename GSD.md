# GSD.md — Guia de Execução do Projeto

Este documento define como o `private-ai-companion` deve ser implementado por uma IA de desenvolvimento, especialmente o Codex.

## 1. Regra principal

O desenvolvimento deve ocorrer por fases. Dentro de uma fase, o Codex pode agir com autonomia operacional. Ao final da fase, deve parar e pedir confirmação para avançar.

## 2. Política de autonomia

O Codex pode, dentro da fase atual:

- criar arquivos;
- criar branches;
- fazer commits;
- rodar comandos de validação;
- corrigir problemas encontrados;
- atualizar documentação;
- reorganizar arquivos quando necessário e justificado;
- fazer push/pull quando configurado.

O Codex não pode:

- avançar para a próxima fase sem confirmação;
- ignorar falhas de qualidade;
- violar `SECURITY.md`;
- alterar decisões arquiteturais aceitas sem criar nova ADR;
- transformar o projeto em algo específico para uma pessoa;
- adicionar live/streaming como eixo central;
- implementar ações perigosas fora da política.

## 3. Fases oficiais

1. Fase 00 — Repositório e documentação inicial
2. Fase 01 — Fundação Python e qualidade
3. Fase 02 — Runtime, bootstrap e event bus
4. Fase 03 — Interação por texto com Rich/Pyfiglet
5. Fase 04 — Persona e prompt builder configurável
6. Fase 05 — LLM router híbrido e providers
7. Fase 06 — Memória local SQLite
8. Fase 07 — TTS, fila de fala e interrupção
9. Fase 08 — STT local com faster-whisper
10. Fase 09 — Avatar com VTube Studio/Live2D
11. Fase 10 — Visão de tela com política de privacidade
12. Fase 11 — Ações locais seguras
13. Fase 12 — Sistema de skills/plugins
14. Fase 13 — UI complementar: tray/dashboard
15. Fase 14 — Observabilidade, logs, replay e health checks
16. Fase 15 — Empacotamento, setup e release
17. Fase 16 — Hardening final e auditoria completa

## 4. Definição de pronto por fase

Uma fase só está pronta quando:

- todo o escopo da fase foi implementado;
- testes relevantes existem;
- validações passam;
- documentação afetada foi atualizada;
- decisões novas foram registradas em ADR quando necessário;
- commits foram feitos de forma organizada;
- relatório final da fase foi apresentado.

## 5. Formato obrigatório do relatório de fase

```text
Fase X — Nome da fase concluída

Objetivo:
- ...

Resumo do que foi feito:
- ...

Arquivos criados:
- ...

Arquivos alterados:
- ...

Validações executadas:
- ...

Resultados das validações:
- ...

Problemas encontrados:
- ...

Decisões/ADRs:
- ...

Commits:
- ...

Pendências:
- ...

Fase X concluída. Posso prosseguir para a Fase Y?
```

## 6. Critérios de bloqueio

A fase deve ser bloqueada se:

- testes obrigatórios falharem;
- lint falhar;
- typecheck falhar;
- houver segredo versionado;
- houver violação de boundary arquitetural;
- o LLM executar ação diretamente;
- o projeto ficar dependente de caminho pessoal;
- houver mudança de escopo sem documentação;
- uma ação local ignorar `safety/`.

## 7. Atualização de documentação

Toda mudança relevante deve atualizar pelo menos um destes documentos:

- `ARCHITECTURE.md`
- `SDD.md`
- `SECURITY.md`
- `docs/modules/*.md`
- `docs/architecture/adr/*.md`
- `docs/workflows/*.md`

## 8. Filosofia

O objetivo não é apenas fazer funcionar. O objetivo é construir um projeto open-source sustentável, claro e seguro, capaz de ser mantido por humanos e agentes de IA ao longo do tempo.

## 9. Requisito de inicialização amigável

O Codex deve implementar um fluxo de inicialização amigável para usuário final no Windows. O projeto deve ter um `Start.bat` robusto ou launcher equivalente quando chegar às fases de fundação/empacotamento.

O `Start.bat` deve ser tratado como requisito de UX e release, não como detalhe opcional. Ele deve iniciar o projeto sem exigir que o usuário comum conheça comandos técnicos.

O projeto não deve ser considerado pronto para release final enquanto o fluxo `Start.bat → aplicação iniciada` não estiver validado.
