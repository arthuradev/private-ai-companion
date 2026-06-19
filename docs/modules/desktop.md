# Módulo `desktop`

## Responsabilidade

Gerencia observação limitada de janela, abertura de apps permitidos, notas locais e ações seguras no desktop.

## Estado na Fase 11

A Fase 11 implementa:

- `DesktopActionService` como orquestrador de ações locais;
- `DesktopActionExecutor` como port para adapters concretos;
- `DesktopPermissionPolicy` para permissões específicas de desktop;
- `SafeLocalDesktopExecutor` como adapter padrão seguro.

O executor padrão:

- cria notas apenas no diretório configurado;
- simula abertura de apps allowlisted;
- retorna título de janela simulado;
- não executa shell;
- não usa automação livre de mouse/teclado;
- não lê arquivos privados.

## Regras

- Deve respeitar boundaries definidos em `docs/architecture/module-boundaries.md`.
- Deve ter testes unitários quando houver comportamento próprio.
- Deve expor contratos claros quando usado por outros módulos.
- Não deve acessar recursos externos sem adapter/policy apropriado.
- Não deve executar ação sem passar por `safety/`.
- Não deve guardar parâmetros sensíveis em eventos ou audit log.

## Entradas esperadas

- Eventos internos.
- Configuração validada.
- Contratos de outros módulos, quando necessário.

## Saídas esperadas

- Eventos internos.
- Resultados tipados.
- Logs estruturados quando relevante.
- Audit records sanitizados.

## Erros comuns a evitar

- Misturar responsabilidades.
- Depender de provider concreto sem adapter.
- Ignorar segurança/privacidade.
- Criar estado global escondido.
- Chamar shell, mouse ou teclado diretamente.
