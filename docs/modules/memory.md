# Módulo `memory`

## Responsabilidade

Gerencia SQLite, memória curta/sessão/longa, política de memória, recuperação, sumarização, edição, exclusão e retenção.

## Implementado na Fase 06

- Modelos tipados de candidata, registro, sensibilidade, status e fonte.
- Policy determinística para decidir entre rejeição, revisão pendente e aprovação.
- Repository SQLite com schema local.
- Busca simples em memórias aprovadas.
- Audit log de decisões sem registrar conteúdo sensível no log.
- Serviço de revisão para aprovar, rejeitar, editar e apagar memórias.
- Redação de candidatas sensíveis rejeitadas antes de persistir.

A conversa por texto ainda não grava memórias automaticamente. Integrações com
sumarização, recuperação semântica e UI de revisão ficam para fases futuras.

## Estado na Fase 13

O bootstrap monta `MemoryReviewService` a partir de `configs/memory.default.toml`
ou de `--memory-config`. O dashboard local consulta a aplicação para obter
contagens por status, sem importar `memory/` dentro de `ui/` e sem renderizar
conteúdo privado bruto por padrão.

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
