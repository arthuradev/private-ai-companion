# Módulo `avatar`

## Responsabilidade

Gerencia estado visual, expressões, lipsync, idle behavior e adapters como VTube Studio.

## Implementado na Fase 09

- Modelos tipados para expressões, requests, resultados, idle e lipsync.
- Port `AvatarProvider`.
- `AvatarService` para aplicar expressões, idle e frames de lipsync.
- Provider fake local para testes e bootstrap.
- Adapter VTube Studio opt-in via WebSocket API.
- Eventos `AvatarStateRequested`, `AvatarStateApplied` e
  `AvatarLipsyncUpdated`.
- CLI `--avatar-expression` para validação manual sem dashboard.

## Expressões padrão

- `idle`
- `listening`
- `thinking`
- `speaking`
- `interrupted`
- `happy`
- `curious`
- `concerned`
- `confused`
- `neutral`

O projeto não define uma identidade visual fixa. Hotkeys, expressões, modelo e
parâmetros de lipsync devem ser configuráveis por usuário/projeto.

## VTube Studio

O adapter VTube Studio fica em `adapters/avatar/` e usa a API pública local via
WebSocket. Ele pode:

- autenticar usando token local;
- acionar hotkeys configuradas por expressão;
- injetar parâmetro de lipsync configurável.

Por padrão, o provider ativo é `fake-avatar`; VTube Studio só é chamado quando
`avatar.provider_id = "vtube-studio"` e o extra opcional `avatar` estiver
instalado.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.

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
