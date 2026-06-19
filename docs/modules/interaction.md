# Módulo `interaction`

## Responsabilidade

Gerencia turnos de conversa, entrada/saída, interrupção, roteamento de texto/voz e coordenação multimodal.

## Implementado na Fase 03

- Serviço de interação por texto.
- Turno local com mensagem do usuário e resposta da companion.
- Publicação dos eventos `UserTextReceived` e `AssistantTextReady`.
- Responder local temporário da Fase 03, sem LLM, prompt builder ou memória.

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
