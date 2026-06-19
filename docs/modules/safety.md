# Módulo `safety`

## Responsabilidade

Gerencia risco, privacidade, permissões, dry-run, confirmação, secrets guard e audit log.

## Estado na Fase 11

A Fase 11 implementa o primeiro pipeline de safety para ações locais:

- `RiskClassifier`;
- `ActionPolicy`;
- `InMemoryActionAuditLog`;
- modelos de intenção, decisão, execução e auditoria.

Regras implementadas:

- ações desconhecidas são classificadas como críticas;
- ações críticas são bloqueadas por padrão;
- ações altas são bloqueadas por padrão;
- ações médias exigem confirmação por padrão;
- audit records não armazenam parâmetros da ação.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.
- Não deve depender de `desktop/`, `brain/`, UI ou adapters concretos.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- Contratos de outros módulos, quando necessário.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
