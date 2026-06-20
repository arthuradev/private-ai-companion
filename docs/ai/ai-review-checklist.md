# Checklist de Revisão por IA

Use este checklist antes de encerrar uma fase.

## Arquitetura

- [ ] `core/` continua pequeno e desacoplado.
- [ ] Novos providers estão atrás de contratos.
- [ ] Novas skills passam por registry e policy.
- [ ] UI não contém regra de negócio.
- [ ] Não há importações circulares.

## Segurança

- [ ] Nenhum segredo foi versionado.
- [ ] Ações locais passam por `safety/`.
- [ ] Dados sensíveis são redigidos em logs.
- [ ] Observabilidade não expõe texto, prompts, screenshots ou parâmetros privados.
- [ ] Screenshot/vision respeitam policy.
- [ ] Memória permanente respeita policy.

## Qualidade

- [ ] Testes foram adicionados/atualizados.
- [ ] Lint passa.
- [ ] Typecheck passa.
- [ ] Erros não são engolidos sem contexto.
- [ ] Documentação foi atualizada.

## Produto

- [ ] O projeto continua público e neutro.
- [ ] A personagem continua personalizável.
- [ ] Não há dependência de hardware pessoal.
- [ ] Não há integração de live como eixo central.
