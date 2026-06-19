# Módulo `skills`

## Responsabilidade

Gerencia sistema de skills/plugins com manifests, registry, permissions e testes de contrato.

Na Fase 12, o módulo implementa o primeiro sistema funcional de skills:

- `BaseSkill`: contrato assíncrono para skills;
- `SkillManifest`: identificação, versão, permissões e tipos de ação permitidos;
- `SkillRegistry`: registro tipado com validação de manifest;
- `SkillManager`: execução governada por policy;
- skills embutidas `builtin.status`, `builtin.local_note` e
  `builtin.open_allowed_app`.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.
- Não deve executar efeitos diretamente quando eles representarem ação local.
- Não deve importar `desktop/`, `ui/`, `adapters/`, `avatar/`, `memory/`,
  `speech/` ou `vision/`.
- Deve delegar efeitos de desktop para um executor externo montado em
  `bootstrap/`, para preservar boundaries.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- `SkillRequest` com input estruturado pelo chamador.
- Contratos de efeitos, quando necessário.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.
- `SkillRunResult` com status, mensagem, output e resultados dos efeitos.

## Fluxo na Fase 12

```text
CLI ou serviço interno
→ SkillRequest
→ SkillManager
→ SkillPolicy
→ BaseSkill.invoke
→ SkillEffectExecutor
→ DesktopActionService quando houver ação local
→ SkillRunResult
```

Eventos publicados:

- `SkillInvoked`;
- `SkillDenied`;
- `SkillCompleted`.

Esses eventos não carregam o input da skill, corpo de nota, parâmetros de ação
ou qualquer segredo. Eles registram apenas skill id, request id, source, status,
reason e contagem de efeitos.

## Skills embutidas

- `builtin.status`: retorna estado local simples para diagnóstico.
- `builtin.local_note`: solicita criação de nota local usando
  `desktop.create_note`.
- `builtin.open_allowed_app`: solicita abertura simulada de app allowlisted
  usando `desktop.open_allowed_app`.

As duas skills com efeito local passam pelo mesmo pipeline de segurança de
ações locais usado pela CLI de desktop. Dry-run, confirmação, risk policy,
permissions e audit log continuam fora da skill.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
- Tratar manifest como mecanismo de autorização suficiente.
- Permitir que uma skill chame shell, sistema de arquivos livre, rede ou APIs
  externas sem port, policy e consentimento explícito.
