# Política de Memória

## Tipos de memória

- Curta: contexto imediato.
- Sessão: conversa atual.
- Longa: fatos e preferências persistentes.
- Candidata: sugestão de memória ainda não aprovada.
- Sensível: protegida, temporária ou rejeitada.

## Regra inicial

Memória automática pode existir, mas deve ser revisável. O usuário deve poder editar e apagar memórias.

## Metadados obrigatórios

- Fonte.
- Timestamp.
- Sensibilidade.
- Confiança.
- Status de aprovação.
- Histórico de alteração.

## Não salvar automaticamente

- Senhas.
- Tokens.
- Dados bancários.
- Informações altamente sensíveis.
- Conteúdo de tela sem permissão.

## Implementado na Fase 06

- Candidatas de baixa sensibilidade ficam pendentes por padrão.
- Candidatas de alta sensibilidade ou sensíveis são rejeitadas por padrão.
- Candidatas sensíveis rejeitadas são persistidas apenas com conteúdo redigido.
- Audit log registra ação, status, motivo e timestamp, não conteúdo integral.
- Aprovação, rejeição, edição e exclusão exigem chamada explícita ao serviço de
  revisão.
