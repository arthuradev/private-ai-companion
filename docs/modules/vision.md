# Módulo `vision`

## Responsabilidade

Gerencia screenshot autorizado, contexto visual temporário, redaction e vision providers.

## Estado na Fase 10

A Fase 10 implementa o pacote `vision/` com:

- `ScreenCaptureProvider` para uma captura explícita;
- `VisionProvider` para análise de contexto visual temporário;
- `ImageRedactor` para redaction de metadados de texto visível;
- `ScreenCapturePolicy` para bloquear captura sem autorização, captura contínua,
  persistência de screenshot e análise externa por padrão;
- `VisionService` para orquestrar policy, captura, redaction, análise e eventos.

O bootstrap usa providers fake locais:

```text
src/private_ai_companion/adapters/vision/fake_capture.py
src/private_ai_companion/adapters/vision/fake_vision.py
```

Eles não acessam tela real, não chamam rede e servem para testes e
desenvolvimento até que adapters reais sejam adicionados com policy própria.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.
- Não deve persistir screenshots por padrão.
- Não deve emitir eventos com bytes de imagem ou texto visual cru.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- Contratos de outros módulos, quando necessário.
- Solicitação explícita do usuário para contexto de tela.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.
- `VisualContext` temporário.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
- Transformar captura de tela em observação contínua.
