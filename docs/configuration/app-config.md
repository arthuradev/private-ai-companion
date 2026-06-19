# app-config

## Responsabilidade

Configuração geral da aplicação: modo de execução, idioma padrão, UI inicial, paths e comportamento de startup.

## Regras

- Configuração versionável não deve conter segredos.
- Valores sensíveis devem vir de `.env` ou armazenamento seguro.
- Configurações devem ser validadas por modelos tipados.
- Defaults devem ser seguros para projeto público.
- O usuário deve conseguir personalizar sem alterar código.

## Deve documentar

- campos disponíveis;
- valores padrão;
- exemplos seguros;
- impacto de privacidade;
- impacto de performance;
- fallback quando ausente.

## Startup e launcher

A configuração geral deve prever opções relacionadas à inicialização, como:

- modo padrão da UI;
- exibição de banner;
- nível de verbosidade no startup;
- caminho de logs;
- modo diagnóstico;
- comportamento quando provedores opcionais não estiverem configurados.

Essas configurações devem ser consumidas pelo bootstrap Python. O `Start.bat` deve apenas repassá-las ou chamar o entrypoint oficial, sem duplicar lógica de configuração.
