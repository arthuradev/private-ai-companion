# persona-config

## Responsabilidade

Configuração da personagem: nome, tom, estilo, idioma, proatividade, limites e voz preferida.

## Arquivo padrão

A Fase 04 adiciona:

```text
configs/persona.default.toml
```

Esse arquivo é versionável, não contém segredos e serve como exemplo seguro. O
usuário pode criar outro TOML e iniciar a aplicação com:

```text
uv run private-ai-companion --persona-config caminho/para/persona.toml
```

ou pelo launcher:

```text
Start.bat --persona-config caminho\para\persona.toml
```

## Campos atuais

- `display_name`: nome exibido na CLI.
- `short_description`: descrição curta da persona.
- `primary_language`: idioma principal.
- `tone`: tom de fala.
- `speaking_style`: lista de traços de estilo.
- `proactivity`: nível textual de proatividade.
- `boundaries`: limites comportamentais da persona.
- `voice_id`: identificador opcional para fases futuras de voz.
- `avatar_id`: identificador opcional para fases futuras de avatar.

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
