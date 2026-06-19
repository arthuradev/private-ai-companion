# Níveis de Risco

## Baixo

- Mudar expressão.
- Falar resposta.
- Abrir painel.

## Médio

- Abrir app permitido.
- Criar nota local.
- Ler título de janela.
- Capturar screenshot manual.

## Alto

- Enviar screenshot para API.
- Abrir URL externa.
- Ler arquivo local selecionado.
- Usar clipboard.

## Crítico

- Apagar arquivo.
- Instalar programa.
- Rodar shell.
- Alterar sistema.
- Acessar senhas/tokens.

## Regra

Crítico é proibido até existir política específica, testes e confirmação explícita.

## Estado na Fase 11

Mapeamento inicial em código:

- baixo: `avatar.set_expression`, `speech.speak_response`, `ui.open_panel`;
- médio: `desktop.open_allowed_app`, `desktop.create_note`,
  `desktop.read_active_window_title`, `vision.capture_manual_screenshot`;
- alto: `desktop.open_url`, `desktop.read_file`, clipboard;
- crítico: shell, apagar arquivo, instalar programa, alterar sistema, ler
  segredos e automação livre de mouse/teclado.

Ações desconhecidas são tratadas como críticas por segurança.
