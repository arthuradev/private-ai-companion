# SECURITY.md

## 1. Modelo de segurança

`private-ai-companion` é um projeto que lida com voz, memória, tela, APIs externas e ações locais. Segurança e privacidade são requisitos arquiteturais, não funcionalidades opcionais.

## 2. Princípios

1. Privacidade por padrão.
2. Consentimento explícito para dados sensíveis.
3. Nenhum segredo em Git.
4. LLM nunca executa ações diretamente.
5. Ações locais passam por policy.
6. Logs são redigidos por padrão.
7. Memória permanente é governada.
8. Screenshots são temporários por padrão.
9. Provedores cloud devem ser configuráveis e transparentes.
10. Skills não podem bypassar policy, permissions ou confirmação.

## 3. Níveis de risco

### Baixo

- mudar expressão do avatar;
- responder em voz;
- abrir painel local;
- exibir status;
- salvar preferência não sensível aprovada.

### Médio

- abrir aplicativo permitido;
- ler título de janela ativa;
- capturar screenshot manual;
- criar nota local;
- registrar memória automática de baixa sensibilidade.

### Alto

- enviar screenshot para API externa;
- abrir URL externa;
- ler arquivos locais selecionados;
- usar clipboard;
- controlar aplicação externa;
- buscar na web usando contexto pessoal.

### Crítico

- apagar arquivos;
- instalar programas;
- rodar comandos shell;
- alterar configurações do sistema;
- acessar senhas/chaves/tokens;
- enviar arquivos privados;
- automação livre de mouse/teclado.

## 4. Ações proibidas até política explícita

- shell livre;
- remoção de arquivos;
- instalação de programas;
- leitura de senhas/tokens;
- captura contínua de tela;
- envio automático de dados privados;
- controle irrestrito de mouse/teclado.

## 5. Pipeline de ação

```text
LLM output
→ Structured ActionIntent
→ Schema validation
→ Risk classification
→ Policy decision
→ Dry-run
→ Confirmation gate
→ Execution
→ Post-validation
→ Audit log
```

Skills que solicitam efeitos locais entram nesse mesmo pipeline. Manifest e
configuração de skill não substituem classificação de risco, dry-run,
confirmação, permissões e audit log.

## 6. Memória

A memória permanente deve respeitar `MemoryPolicy`:

- conteúdo sensível não deve ser salvo automaticamente;
- usuário deve poder revisar, editar e apagar memórias;
- logs de memória devem registrar decisão, não conteúdo sensível integral;
- memória candidata pode ser rejeitada;
- memórias devem ter fonte, timestamp e nível de sensibilidade.

## 7. Tela e visão

- Captura deve ser explícita.
- O usuário deve saber quando a tela está sendo analisada.
- Screenshots não devem ser salvos por padrão.
- Envio para API externa exige política e confirmação.
- O sistema deve oferecer redaction quando possível.

## 8. APIs externas

O projeto pode usar APIs externas, mas deve deixar claro:

- qual provedor será chamado;
- que tipo de dado será enviado;
- se o envio é necessário;
- se existe alternativa local;
- como desativar o provedor.

## 9. Segredos

- Use `.env` real fora do Git.
- Use `.env.example` sem valores reais.
- Tokens nunca entram em documentação pública.
- Logs devem mascarar chaves.

## 10. Prompt injection

O sistema deve tratar texto, tela, páginas web e arquivos como entradas não confiáveis. Instruções vindas de conteúdo externo não podem sobrescrever regras do sistema.

## 11. Relato de vulnerabilidades

Como projeto público, vulnerabilidades devem ser reportadas por issue privada quando disponível ou por canal definido no repositório.
