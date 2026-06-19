# Metodologia de Desenvolvimento com IA

## 1. Ideia central

Este projeto deve ser desenvolvido como uma colaboração entre humano e IA. A IA implementa, testa, refatora e documenta; o humano define direção, aprova avanço de fase e decide trade-offs relevantes.

## 2. Modelo de trabalho

```text
Spec → Architecture → Phase Plan → Implementation → Tests → Review → Commit → Phase Gate
```

## 3. Regra de contexto

A IA deve usar os documentos do projeto como fonte de verdade. Prompts no chat não substituem documentação versionada.

## 4. Trabalho por fases

Fases reduzem risco de deriva arquitetural. Cada fase deve ser pequena o suficiente para revisar, mas grande o suficiente para entregar uma capacidade coerente.

## 5. IA como implementadora, não autoridade final

A IA pode sugerir soluções, mas decisões estruturais devem estar registradas em ADRs e respeitar `ARCHITECTURE.md`.

## 6. Documentação viva

Quando o código mudar comportamento, arquitetura, segurança ou fluxo de uso, a documentação deve mudar junto.

## 7. Qualidade antes de velocidade

O objetivo não é ter código o mais rápido possível. O objetivo é ter uma base que continue saudável depois de muitas iterações.
