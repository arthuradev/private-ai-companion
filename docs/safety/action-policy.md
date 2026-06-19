# Política de Ações

## Pipeline

```text
ActionIntent
→ Validate schema
→ Classify risk
→ Check permissions
→ Dry-run
→ Confirm if needed
→ Execute
→ Validate result
→ Audit
```

## Regras

- LLM não executa ações.
- Skills não podem burlar policy.
- Ações críticas são bloqueadas até documentação e implementação específicas.
- Ação média ou alta deve deixar rastro de auditoria.

## Estado na Fase 11

O pipeline implementado para ações locais é:

```text
DesktopActionRequest
→ ActionIntent
→ RiskClassifier
→ ActionPolicy
→ DesktopPermissionPolicy
→ DesktopActionExecutor.dry_run
→ PermissionRequired quando confirmação faltar
→ DesktopActionExecutor.execute quando permitido
→ InMemoryActionAuditLog
```

O executor padrão não aceita comandos shell. Ações críticas como
`system.run_shell`, `system.delete_file` e `secrets.read` são classificadas como
críticas e bloqueadas antes de dry-run ou execução.
