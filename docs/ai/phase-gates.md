# Phase Gates

## Objetivo

Definir os gates obrigatórios ao final de cada fase.

## Gate mínimo

Antes de encerrar uma fase, o Codex deve verificar:

- escopo completo;
- testes relevantes;
- lint/typecheck;
- documentação atualizada;
- commits feitos;
- riscos registrados;
- nenhuma violação de segurança;
- nenhuma violação de arquitetura.

## Gate de segurança

Obrigatório quando a fase tocar:

- memória;
- visão;
- desktop;
- skills;
- APIs externas;
- logs;
- segredos.

## Gate de arquitetura

Obrigatório quando a fase criar módulo, adapter, provider, skill, evento ou boundary novo.

## Saída esperada

O Codex deve gerar relatório claro e pedir permissão para avançar.
