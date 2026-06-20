# Estratégia de Testes

## Tipos de teste

- Unitários: regras puras e módulos isolados.
- Integração: fluxos entre módulos.
- Contrato: providers, adapters e skills.
- Segurança: memory policy, action policy, privacy guard.
- Arquitetura: boundaries e importações proibidas.
- E2E: poucos fluxos completos.

## Testes prioritários

1. Event bus.
2. Config loader.
3. Prompt builder.
4. LLM router com fake provider.
5. Memory policy.
6. Action policy.
7. Skill manifest validation.
8. Screen capture policy.
9. TTS queue interruption.
10. Avatar state mapping.
11. Dashboard/tray snapshots sem dados sensíveis.
12. Observability redaction em replay de eventos e logs estruturados.
13. Health checks locais sem dependência de providers externos.

## Regra

Módulos de segurança devem ter testes antes ou junto da implementação.
Fluxos de observabilidade devem provar que payloads privados não aparecem por
padrão em logs, snapshots ou replay de eventos.
