# Painel de Controle de Tarefas

Aplicacao Flask com autenticacao, SQLite, CRUD de tarefas, API JSON, filtros por status, modo escuro e dashboard com Chart.js.

## Como executar

```bash
pip install -r requirements.txt
python app.py
```

Depois acesse `http://127.0.0.1:5000`.

## Rotas principais

- `/registro` - cadastro de usuario.
- `/login` - entrada do usuario.
- `/logout` - saida.
- `/dashboard` - painel de tarefas.
- `/nova_tarefa` - criacao.
- `/editar/<id>` - edicao.
- `/excluir/<id>` - remocao.
- `/progresso` - dashboard visual.
- `/api/tasks` - lista/cria tarefas em JSON.
- `/api/tasks/<id>` - consulta, altera ou remove uma tarefa em JSON.
- `/api/stats` - dados para o grafico.
