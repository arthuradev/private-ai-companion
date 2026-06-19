# ADR 0015 — Usar Start.bat como entrypoint amigável no Windows

## Status

Aceito.

## Contexto

O `private-ai-companion` é um projeto público, mas a experiência de uso deve ser amigável para pessoas que não querem abrir terminal ou memorizar comandos. Como o projeto é Windows-first, um arquivo `Start.bat` robusto reduz atrito de uso, facilita testes manuais e torna a aplicação mais acessível para usuários finais.

Ao mesmo tempo, o launcher não pode virar local de regra de negócio, automação perigosa ou configuração secreta. Ele deve apenas preparar o ambiente e iniciar o entrypoint oficial da aplicação.

## Decisão

O projeto deve fornecer um `Start.bat` como entrypoint amigável para Windows.

O `Start.bat` deve:

- detectar ambiente básico;
- iniciar o fluxo oficial do projeto;
- exibir mensagens claras;
- lidar com falhas comuns de setup;
- preservar logs;
- não conter lógica de produto;
- não executar ações destrutivas;
- não armazenar segredos.

O entrypoint real da aplicação continua sendo o pacote Python, por exemplo `python -m private_ai_companion` ou comando equivalente configurado em `pyproject.toml`.

## Consequências positivas

- Usuários finais não precisam digitar comandos técnicos.
- O projeto fica mais acessível no Windows.
- O fluxo de inicialização fica padronizado.
- Diagnóstico de startup fica mais simples.

## Consequências negativas

- É necessário manter um launcher específico para Windows.
- O projeto precisará testar cenários de bootstrap além dos testes Python.
- O Codex deve evitar colocar lógica demais no `.bat`.

## Regras

- O launcher é borda operacional, não núcleo.
- O launcher pode chamar scripts auxiliares, mas não deve implementar regras do produto.
- O launcher deve falhar de forma clara e segura.
- O launcher deve ser documentado em `docs/runtime/startup-launcher.md`.
