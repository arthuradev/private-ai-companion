# Fase 15 — Empacotamento, setup e release

## Objetivo

Preparar empacotamento, documentação de instalação e release/tag.

## Escopo

Esta fase deve implementar apenas o necessário para cumprir seu objetivo, sem antecipar funcionalidades de fases futuras além de contratos ou placeholders claramente justificados.

## Atividades esperadas

- Revisar documentos relevantes.
- Criar/alterar arquivos necessários.
- Adicionar testes correspondentes.
- Atualizar documentação afetada.
- Executar validações.
- Fazer commits organizados.

## Validações mínimas

Quando houver código:

- `ruff format --check`
- `ruff check`
- `pytest`
- `pyright`

Quando a fase tocar segurança, memória, visão, desktop ou skills, incluir testes específicos de segurança/policy.

## Critérios de conclusão

- Escopo da fase concluído.
- Validações executadas.
- Documentação atualizada.
- Nenhuma violação arquitetural conhecida.
- Relatório de fase apresentado.
- Codex parou e pediu autorização para a próxima fase.

## Relatório obrigatório

Ao terminar, apresentar:

```text
Fase 15 concluída.

Resumo:
- ...

Arquivos criados/alterados:
- ...

Validações:
- ...

Problemas:
- ...

Commits:
- ...

Fase 15 concluída. Posso prosseguir para a próxima fase?
```

## Requisito obrigatório — launcher de usuário final

Esta fase deve endurecer e validar o `Start.bat` como caminho oficial de inicialização para usuários Windows.

O Codex deve validar pelo menos:

- execução normal pelo `Start.bat`;
- comportamento quando `.env` não existe;
- comportamento quando provedores opcionais não estão configurados;
- comportamento quando dependências precisam ser sincronizadas;
- logs de startup;
- mensagem clara em falha;
- ausência de segredos no launcher;
- ausência de lógica de produto no launcher.

O release não deve ser considerado pronto se o usuário precisar conhecer comandos técnicos para iniciar a aplicação.
