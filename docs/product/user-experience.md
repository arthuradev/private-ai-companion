# Experiência do Usuário

## Princípios de UX

- Presença sem invasão.
- Respostas curtas quando apropriado.
- Voz natural e cancelável.
- Expressões coerentes.
- Estado visível: ouvindo, pensando, falando, ociosa.
- Permissões claras.
- Configuração simples.

## Fluxo inicial esperado

1. Usuário inicia app.
2. CLI exibe banner Rich/Pyfiglet com nome do projeto.
3. Sistema carrega configuração.
4. Companion entra em estado idle.
5. Usuário conversa por texto ou voz.
6. Companion responde por texto, voz e avatar.
7. Memória candidata é tratada por policy.
8. Ações locais pedem confirmação quando necessário.

## Proatividade

A companion pode ter comportamento proativo desde o começo, mas configurável e respeitoso. Proatividade deve começar baixa e nunca envolver captura oculta de dados.

## Inicialização sem comandos técnicos

O fluxo padrão para usuário final no Windows deve ser abrir `Start.bat`. O projeto pode oferecer comandos técnicos para desenvolvedores, mas eles não devem ser necessários para uso normal.

Experiência esperada:

```text
usuário executa Start.bat
→ sistema valida ambiente
→ aplicação abre com banner Rich/Pyfiglet
→ status de carregamento aparece
→ companion fica pronta para interação
```

Falhas de ambiente devem ser explicadas em linguagem clara. O usuário não deve receber apenas stack trace ou erro cru de terminal.
