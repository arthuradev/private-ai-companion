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
