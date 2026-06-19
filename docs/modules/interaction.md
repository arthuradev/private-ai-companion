# Módulo `interaction`

## Responsabilidade

Gerencia turnos de conversa, entrada/saída, interrupção, roteamento de texto/voz e coordenação multimodal.

## Implementado na Fase 03

- Serviço de interação por texto.
- Turno local com mensagem do usuário e resposta da companion.
- Publicação dos eventos `UserTextReceived` e `AssistantTextReady`.
- Responder local temporário da Fase 03, sem LLM ou memória.

## Atualizado na Fase 04

- Cada turno de texto passa pelo context builder e prompt builder.
- A resposta local usa a persona carregada para exibir o nome configurado.
- O prompt é montado internamente para testes e futura integração com LLM, mas
  ainda não é enviado para provider externo.

## Atualizado na Fase 05

- A resposta do turno passa pelo `LLMRouter`.
- O provider padrão é fake/local e não chama rede.
- Providers externos reais continuam desabilitados e planejados.

## Atualizado na Fase 08

- `VoiceInteractionService` recebe resultado de `VoiceInputService`.
- Transcrições aceitas por STT são convertidas em turnos normais de texto.
- Entradas de voz ignoradas por VAD, STT desabilitado ou transcrição vazia não
  chamam o fluxo de resposta.
- A UI não importa `speech/`; ela chama métodos públicos da aplicação.

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
