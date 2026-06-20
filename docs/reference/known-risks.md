# Riscos Conhecidos

## Riscos técnicos

- Latência alta em STT/LLM/TTS.
- Complexidade de áudio no Windows.
- Dependência de APIs externas.
- Setup de GPU/CUDA.
- Integração VTube Studio instável.

## Riscos de segurança

- Prompt injection.
- Logs com dados sensíveis.
- Replay de eventos ou diagnóstico expondo payload privado.
- Memória permanente ruim.
- Screenshots enviados indevidamente.
- Skills burlando policy.

## Riscos de arquitetura

- Orquestrador virar arquivo gigante.
- Avatar controlar fluxo.
- Providers invadirem core.
- Skills sem manifest.
- Configuração espalhada.

## Mitigação

- Boundaries.
- Tests.
- Safety policy.
- Redaction determinística em observabilidade.
- ADRs.
- Phase gates.
- Revisão contínua.
