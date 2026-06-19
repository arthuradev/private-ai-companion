# Prompt Engineering do Projeto

## Objetivo

Definir como prompts permanentes e dinâmicos devem ser tratados no projeto.

## Tipos de prompt

### Prompt de sistema/persona

Define identidade, tom, limites e estilo da personagem.

### Prompt de contexto

Contém informações de sessão, memória recuperada, estado atual, visão autorizada e instruções específicas do turno.

### Prompt de ferramenta/ação

Define como o LLM deve produzir intenções estruturadas, sem executar ações diretamente.

## Regras

- Prompts devem ser versionáveis quando forem parte do produto.
- Personalidade deve ser configurável em arquivo próprio.
- Prompt não é mecanismo de segurança.
- Regras críticas devem existir também em código/policy.
- Prompt builder deve ter testes de snapshot.
- Memórias sensíveis não devem entrar automaticamente no prompt.

## Personalização

O projeto deve oferecer uma personalidade padrão carinhosa/próxima, mas permitir substituição por configuração.

## Implementado na Fase 04

O prompt builder gera uma estrutura testável com:

- mensagem `system` contendo persona, tom, estilo, proatividade e limites;
- mensagem `user` contendo o contexto do turno;
- aviso explícito de que conteúdo do usuário é dado não confiável;
- texto renderizado por `PromptBundle.as_text()` para snapshots e depuração.

O prompt builder não executa ações, não decide segurança e não chama providers
externos.

## Evitar

- Prompt gigante impossível de testar.
- Misturar persona, segurança, memória e ferramentas em texto único sem estrutura.
- Deixar instruções de tool use virem permissão de execução.
