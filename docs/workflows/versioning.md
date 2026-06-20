# Versionamento

O projeto usa SemVer.

```text
MAJOR.MINOR.PATCH
```

O pacote Python usa versões PEP 440 em `pyproject.toml` e
`src/private_ai_companion/__init__.py`. Quando houver release candidate, a versão
Python deve ser convertida para tag SemVer:

```text
0.3.0rc1 → v0.3.0-rc.1
```

## Planejamento

- `v0.1.0`: primeira versão funcional com conversa, voz, memória e avatar.
- `v0.2.0`: visão, desktop actions seguras e skills.
- `v0.3.0`: dashboard/tray, empacotamento e hardening.
- `v1.0.0`: release estável.

## Estado atual

- Pacote Python: `0.3.0`.
- Tag SemVer estável da Fase 16: `v0.3.0`.
- Release candidate anterior preservado como `v0.3.0-rc.1`.

## Tags

Tags devem ser anotadas quando possível e acompanhadas de changelog.
