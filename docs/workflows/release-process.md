# Processo de Release

## Antes de release

- Todos os testes passam.
- Lint passa.
- Typecheck passa.
- Documentação atualizada.
- Changelog atualizado.
- Segurança revisada.
- Dados privados ausentes.
- Config examples revisados.

## Passos

1. Atualizar `CHANGELOG.md`.
2. Confirmar versão.
3. Rodar validações.
4. Criar tag SemVer.
5. Publicar release no GitHub.
6. Incluir notas de release.

## Validação de launcher

Antes de publicar release, validar o fluxo de usuário final:

```text
Start.bat → aplicação inicia → banner Rich/Pyfiglet aparece → companion fica pronta ou informa configuração ausente com clareza
```

O release não deve ser publicado se o launcher estiver quebrado, exigir comando técnico manual ou ocultar falhas importantes.
