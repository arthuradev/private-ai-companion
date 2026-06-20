# Módulo `ui`

## Responsabilidade

Gerencia CLI Rich/Pyfiglet, tray app e dashboard, sem conter regra de negócio.

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

## Relação com Start.bat

O `Start.bat` é entrypoint operacional para usuário final, mas a UI real continua dentro do módulo `ui/` e do bootstrap Python.

A CLI inicial deve usar Rich + Pyfiglet e exibir o nome `private-ai-companion` ao iniciar. O launcher apenas inicia essa experiência; ele não implementa a interface.

## Implementado na Fase 03

- Banner inicial com Pyfiglet.
- Renderização com Rich.
- Loop de conversa por texto.
- Comandos de saída `/exit`, `/quit`, `exit` e `quit`.
- Modo `--once` para executar uma única mensagem e encerrar.

## Implementado na Fase 13

- `RichDashboardApp` para dashboard local em Rich.
- `DashboardSnapshot` com status de runtime, configuração, memória, permissões
  de desktop e skills.
- `RichTrayStatusApp` para o primeiro modelo local de tray/status.
- `TraySnapshot` com tooltip e itens de menu testáveis.
- CLI `--dashboard` para renderizar o dashboard e encerrar.
- CLI `--tray-status` para renderizar o status/menu de tray e encerrar.

O dashboard e o tray status usam apenas a API pública de `Application`. A UI não
importa `memory/`, `desktop/`, `skills/`, `safety/` ou `vision/` diretamente.

O modelo de tray da Fase 13 é local e testável. Integração nativa com a bandeja
do sistema deve continuar sendo uma borda de UI futura, sem regra de negócio e
sem dependência obrigatória para o fluxo principal.

## Implementado na Fase 14

- `RichDiagnosticsApp` para renderizar diagnóstico local em Rich.
- Visualização de health checks, métricas de eventos, replay sanitizado e logs
  estruturados sanitizados.
- CLI `--diagnostics` para renderizar o snapshot de diagnóstico e encerrar.

A tela de diagnóstico usa apenas a API pública de `Application`. A UI não
acessa eventos brutos, não lê logs persistentes e não decide política de
redaction.
