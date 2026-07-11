from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)


def preparar_banco():
    db.create_all()

    # Caso o banco antigo ja exista sem o campo telefone,
    # adiciona a coluna sem apagar os alunos cadastrados.
    inspector = inspect(db.engine)
    colunas = [coluna['name'] for coluna in inspector.get_columns('aluno')]

    if 'telefone' not in colunas:
        db.session.execute(text("ALTER TABLE aluno ADD COLUMN telefone VARCHAR(20) NOT NULL DEFAULT ''"))
        db.session.commit()


@app.route('/')
def index():
    alunos = Aluno.query.order_by(Aluno.id.desc()).all()
    total_alunos = Aluno.query.count()
    return render_template('lista.html', alunos=alunos, total_alunos=total_alunos)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        if not nome or not email or not telefone:
            return render_template(
                'formulario.html',
                titulo='Cadastrar aluno',
                erro='Preencha todos os campos.',
                nome=nome,
                email=email,
                telefone=telefone,
                aluno_id=None
            )

        aluno = Aluno(nome=nome, email=email, telefone=telefone)
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template(
        'formulario.html',
        titulo='Cadastrar aluno',
        erro=None,
        nome='',
        email='',
        telefone='',
        aluno_id=None
    )


@app.route('/editar/<int:aluno_id>', methods=['GET', 'POST'])
def editar(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        if not nome or not email or not telefone:
            return render_template(
                'formulario.html',
                titulo='Editar aluno',
                erro='Preencha todos os campos.',
                nome=nome,
                email=email,
                telefone=telefone,
                aluno_id=aluno.id
            )

        aluno.nome = nome
        aluno.email = email
        aluno.telefone = telefone
        db.session.commit()
        return redirect(url_for('index'))

    return render_template(
        'formulario.html',
        titulo='Editar aluno',
        erro=None,
        nome=aluno.nome,
        email=aluno.email,
        telefone=aluno.telefone,
        aluno_id=aluno.id
    )


@app.route('/excluir/<int:aluno_id>', methods=['POST'])
def excluir(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        preparar_banco()

    app.run(debug=True)
