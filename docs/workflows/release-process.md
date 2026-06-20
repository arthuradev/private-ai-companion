# Processo de Release

## Antes de release

- Todos os testes passam.
- Lint passa.
- Typecheck passa.
- Build de sdist/wheel passa.
- Documentação atualizada.
- Changelog atualizado.
- Segurança revisada.
- Dados privados ausentes.
- Config examples revisados.
- `Start.bat` validado como caminho principal de usuário Windows.

## Passos

1. Atualizar `CHANGELOG.md`.
2. Confirmar versão em `pyproject.toml` e `src/private_ai_companion/__init__.py`.
3. Rodar validações.
4. Gerar artefatos locais com `uv build --sdist --wheel`.
5. Criar tag SemVer.
6. Publicar release no GitHub.
7. Incluir notas de release.

## Validação automatizada local

Mantenedores podem executar:

```text
powershell -ExecutionPolicy Bypass -File scripts/release-check.ps1
```

Esse helper roda lint, formatação, testes e typecheck com `uv run --locked`,
executa build e valida o caminho `Start.bat --diagnostics`. Ele não substitui
revisão humana, auditoria de segurança ou criação da release no GitHub.

## Versão e tag

Versão Python deve seguir PEP 440. Tags públicas devem seguir SemVer.

Exemplo para o release candidate da Fase 15:

```text
Python package: 0.3.0rc1
Git tag: v0.3.0-rc.1
```

A release estável deve aguardar hardening final e auditoria completa.

## Validação de launcher

Antes de publicar release, validar o fluxo de usuário final:

```text
Start.bat → aplicação inicia → banner Rich/Pyfiglet aparece → companion fica pronta ou informa configuração ausente com clareza
```

Também validar:

- `.env` ausente;
- provedores opcionais não configurados;
- dependências sincronizadas pelo `uv` a partir do lockfile;
- `logs/startup.log` criado sem argumentos privados;
- falha clara quando `uv` ou Python 3.12+ não estão disponíveis;
- ausência de segredos e regra de produto no launcher.

O release não deve ser publicado se o launcher estiver quebrado, exigir comando técnico manual ou ocultar falhas importantes.
