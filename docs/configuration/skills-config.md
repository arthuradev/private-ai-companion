# skills-config

## Responsabilidade

Configuração de skills habilitadas, permissões, níveis de risco e manifests.

## Regras

- Configuração versionável não deve conter segredos.
- Valores sensíveis devem vir de `.env` ou armazenamento seguro.
- Configurações devem ser validadas por modelos tipados.
- Defaults devem ser seguros para projeto público.
- O usuário deve conseguir personalizar sem alterar código.

## Deve documentar

- campos disponíveis;
- valores padrão;
- exemplos seguros;
- impacto de privacidade;
- impacto de performance;
- fallback quando ausente.

## Arquivo padrão

```text
configs/skills.default.toml
```

Quando nenhum arquivo é informado, o bootstrap carrega esse default versionado.
O arquivo é público, não contém segredos e habilita apenas skills embutidas
seguras para desenvolvimento local.

## Campos

```toml
[skills]
enabled = true

[[skills.skill]]
skill_id = "builtin.status"
enabled = true
permissions = ["status.read"]
allowed_action_types = []
```

- `skills.enabled`: liga ou desliga o sistema de skills como um todo.
- `skill_id`: id estável do manifest da skill.
- `enabled`: habilita a skill específica.
- `permissions`: permissões concedidas à skill.
- `allowed_action_types`: tipos de ação local que a skill pode solicitar.

## Defaults da Fase 12

- `builtin.status`: habilitada com `status.read`, sem efeitos locais.
- `builtin.local_note`: habilitada com `desktop.action` e
  `desktop.create_note`.
- `builtin.open_allowed_app`: habilitada com `desktop.action` e
  `desktop.open_allowed_app`.

## Validação

O loader rejeita:

- estrutura TOML inválida;
- ids de skill desconhecidos no conjunto suportado pela Fase 12;
- permissões desconhecidas;
- tipos de ação desconhecidos;
- permissões ou actions duplicadas dentro da mesma skill.

Habilitar uma skill na configuração não autoriza execução direta de ação local.
O `SkillManager` verifica permissões e actions declaradas, e efeitos de desktop
ainda passam por `DesktopActionService`, `RiskClassifier`, `ActionPolicy`,
`DesktopPermissionPolicy`, dry-run, confirmação e audit log.

## CLI

Para escolher outro arquivo:

```text
uv run private-ai-companion --skills-config caminho/skills.toml --skill builtin.status
```

No Windows, o mesmo argumento pode ser repassado pelo launcher:

```text
Start.bat --skills-config configs/skills.default.toml --skill builtin.status
```
