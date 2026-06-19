# desktop-config

## Responsabilidade

Configuração de ações locais seguras: executor, ações permitidas, confirmação,
notas locais, leitura limitada de janela e apps allowlisted.

## Regras

- Configuração versionável não deve conter segredos.
- O default deve ser seguro para projeto público.
- Ações críticas devem permanecer bloqueadas.
- Ações médias devem exigir confirmação por padrão.
- Apps permitidos devem ser allowlisted por id estável.
- Caminhos de notas devem ficar em diretório local controlado.

## Estado na Fase 11

A configuração versionável padrão fica em:

```text
configs/desktop.default.toml
```

Campos atuais:

- `desktop.actions.enabled`: habilita ou desabilita ações locais.
- `desktop.actions.executor_id`: executor. Na Fase 11, apenas
  `safe-local-desktop` é executável.
- `desktop.actions.allowed_action_types`: ações permitidas.
- `desktop.actions.require_confirmation_for`: riscos que exigem confirmação.
- `desktop.actions.allow_high_risk`: mantém ações altas bloqueadas por default.
- `desktop.actions.allow_critical_risk`: mantém ações críticas bloqueadas por
  default.
- `desktop.notes.enabled`: habilita criação de notas locais.
- `desktop.notes.directory`: diretório permitido para notas.
- `desktop.notes.max_note_bytes`: limite de tamanho do corpo da nota.
- `desktop.window.active_window_title_enabled`: habilita leitura limitada de
  título de janela.
- `desktop.window.fake_active_window_title`: título simulado usado pelo executor
  seguro padrão.
- `desktop.allowed_apps`: mapa de apps permitidos. Na Fase 11 a abertura é
  simulada pelo executor seguro.

Quando o arquivo está ausente, o bootstrap usa os mesmos defaults seguros do
arquivo versionado.
