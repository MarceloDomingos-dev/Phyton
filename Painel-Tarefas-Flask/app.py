import json
import os
import sqlite3
import urllib.request
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
app.config["DATABASE"] = os.environ.get(
    "DATABASE", os.path.join(app.instance_path, "tarefas.sqlite3")
)

STATUS_OPTIONS = {
    "pendente": "Pendente",
    "andamento": "Em andamento",
    "concluida": "Concluida",
}


def get_db():
    if "db" not in g:
        os.makedirs(app.instance_path, exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',
            usuario_id INTEGER NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        );
        """
    )
    db.commit()


@app.before_request
def ensure_database():
    init_db()
    user_id = session.get("user_id")
    g.user = None
    if user_id:
        g.user = get_db().execute(
            "SELECT id, nome, email FROM usuarios WHERE id = ?", (user_id,)
        ).fetchone()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Faça login para acessar o painel.", "warning")
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


def normalize_status(status):
    return status if status in STATUS_OPTIONS else "pendente"


def row_to_task(row):
    return {
        "id": row["id"],
        "titulo": row["titulo"],
        "descricao": row["descricao"] or "",
        "status": row["status"],
        "status_label": STATUS_OPTIONS.get(row["status"], row["status"]),
        "criado_em": row["criado_em"],
        "atualizado_em": row["atualizado_em"],
    }


def get_user_task(task_id):
    return get_db().execute(
        """
        SELECT id, titulo, descricao, status, criado_em, atualizado_em
        FROM tarefas
        WHERE id = ? AND usuario_id = ?
        """,
        (task_id, g.user["id"]),
    ).fetchone()


def fetch_advice():
    try:
        with urllib.request.urlopen("https://api.adviceslip.com/advice", timeout=4) as res:
            payload = json.loads(res.read().decode("utf-8"))
            return payload["slip"]["advice"]
    except Exception:
        return "Organize uma tarefa por vez e mantenha o foco no proximo passo."


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("registro.html")

        try:
            get_db().execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, generate_password_hash(senha)),
            )
            get_db().commit()
            flash("Cadastro criado. Entre para continuar.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Este e-mail ja esta cadastrado.", "danger")

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        user = get_db().execute(
            "SELECT id, nome, email, senha FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["senha"], senha):
            flash("E-mail ou senha invalidos.", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sessao encerrada.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        advice=fetch_advice(),
        status_options=STATUS_OPTIONS,
    )


@app.route("/progresso")
@login_required
def progresso():
    return render_template("progresso.html")


@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = normalize_status(request.form.get("status", "pendente"))

        if not titulo:
            flash("Informe o titulo da tarefa.", "danger")
            return render_template(
                "tarefa_form.html",
                action_label="Criar tarefa",
                task=None,
                status_options=STATUS_OPTIONS,
            )

        get_db().execute(
            """
            INSERT INTO tarefas (titulo, descricao, status, usuario_id)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, descricao, status, g.user["id"]),
        )
        get_db().commit()
        flash("Tarefa criada com sucesso.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "tarefa_form.html",
        action_label="Criar tarefa",
        task=None,
        status_options=STATUS_OPTIONS,
    )


@app.route("/editar/<int:task_id>", methods=["GET", "POST"])
@login_required
def editar_tarefa(task_id):
    task = get_user_task(task_id)
    if task is None:
        abort(404)

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = normalize_status(request.form.get("status", "pendente"))

        if not titulo:
            flash("Informe o titulo da tarefa.", "danger")
            return render_template(
                "tarefa_form.html",
                action_label="Salvar alteracoes",
                task=task,
                status_options=STATUS_OPTIONS,
            )

        get_db().execute(
            """
            UPDATE tarefas
            SET titulo = ?, descricao = ?, status = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ? AND usuario_id = ?
            """,
            (titulo, descricao, status, task_id, g.user["id"]),
        )
        get_db().commit()
        flash("Tarefa atualizada.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "tarefa_form.html",
        action_label="Salvar alteracoes",
        task=task,
        status_options=STATUS_OPTIONS,
    )


@app.route("/excluir/<int:task_id>", methods=["POST"])
@login_required
def excluir_tarefa(task_id):
    task = get_user_task(task_id)
    if task is None:
        abort(404)

    get_db().execute(
        "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?", (task_id, g.user["id"])
    )
    get_db().commit()
    flash("Tarefa removida.", "info")
    return redirect(url_for("dashboard"))


@app.route("/api/tasks", methods=["GET", "POST"])
@login_required
def api_tasks():
    if request.method == "POST":
        payload = request.get_json(silent=True) or request.form
        titulo = (payload.get("titulo") or "").strip()
        descricao = (payload.get("descricao") or "").strip()
        status = normalize_status(payload.get("status", "pendente"))

        if not titulo:
            return jsonify({"error": "Titulo obrigatorio."}), 400

        cursor = get_db().execute(
            """
            INSERT INTO tarefas (titulo, descricao, status, usuario_id)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, descricao, status, g.user["id"]),
        )
        get_db().commit()
        task = get_user_task(cursor.lastrowid)
        return jsonify(row_to_task(task)), 201

    status = request.args.get("status", "todas")
    params = [g.user["id"]]
    where_status = ""
    if status in STATUS_OPTIONS:
        where_status = "AND status = ?"
        params.append(status)

    rows = get_db().execute(
        f"""
        SELECT id, titulo, descricao, status, criado_em, atualizado_em
        FROM tarefas
        WHERE usuario_id = ? {where_status}
        ORDER BY
            CASE status
                WHEN 'pendente' THEN 1
                WHEN 'andamento' THEN 2
                WHEN 'concluida' THEN 3
                ELSE 4
            END,
            criado_em DESC
        """,
        params,
    ).fetchall()
    return jsonify([row_to_task(row) for row in rows])


@app.route("/api/tasks/<int:task_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_task_detail(task_id):
    task = get_user_task(task_id)
    if task is None:
        return jsonify({"error": "Tarefa nao encontrada."}), 404

    if request.method == "GET":
        return jsonify(row_to_task(task))

    if request.method == "DELETE":
        get_db().execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (task_id, g.user["id"]),
        )
        get_db().commit()
        return jsonify({"ok": True})

    payload = request.get_json(silent=True) or {}
    titulo = (payload.get("titulo") or task["titulo"]).strip()
    descricao = (payload.get("descricao") if "descricao" in payload else task["descricao"])
    status = normalize_status(payload.get("status", task["status"]))

    if not titulo:
        return jsonify({"error": "Titulo obrigatorio."}), 400

    get_db().execute(
        """
        UPDATE tarefas
        SET titulo = ?, descricao = ?, status = ?, atualizado_em = CURRENT_TIMESTAMP
        WHERE id = ? AND usuario_id = ?
        """,
        (titulo, descricao, status, task_id, g.user["id"]),
    )
    get_db().commit()
    return jsonify(row_to_task(get_user_task(task_id)))


@app.route("/api/stats")
@login_required
def api_stats():
    rows = get_db().execute(
        """
        SELECT status, COUNT(*) AS total
        FROM tarefas
        WHERE usuario_id = ?
        GROUP BY status
        """,
        (g.user["id"],),
    ).fetchall()
    stats = {key: 0 for key in STATUS_OPTIONS}
    stats.update({row["status"]: row["total"] for row in rows})
    return jsonify(
        {
            "labels": [STATUS_OPTIONS[key] for key in STATUS_OPTIONS],
            "values": [stats[key] for key in STATUS_OPTIONS],
            "raw": stats,
        }
    )


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug)
