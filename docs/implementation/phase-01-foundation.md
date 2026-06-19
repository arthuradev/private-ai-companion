# Fase 01 — Fundação Python e qualidade

## Objetivo

Criar projeto Python 3.12+, uv, ruff, pytest, pyright e estrutura base.

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
Fase 01 concluída.

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

Fase 01 concluída. Posso prosseguir para a próxima fase?
```

## Requisito adicional — Start.bat inicial

Nesta fase, o Codex deve criar a primeira versão do `Start.bat` na raiz do repositório real.

A versão inicial deve:

- chamar o entrypoint oficial do projeto;
- exibir mensagem clara de startup;
- não conter regra de negócio;
- não conter segredos;
- falhar com mensagem compreensível quando o ambiente estiver ausente;
- ser simples o bastante para evoluir nas fases futuras.

Mesmo que o launcher ainda seja básico nesta fase, sua existência deve ser tratada como requisito arquitetural.
