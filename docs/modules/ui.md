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
