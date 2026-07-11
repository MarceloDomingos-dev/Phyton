from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Rota para as questões da Atividade Jinja
@app.route('/jinja')
def atividade_jinja():
    # Dados de teste para preencher o template
    dados_teste = {
        "nome": "Carlos",
        "idade": 17,
        "usuario": {
            "nome": "Ana", 
            "email": "ana@email.com"
        },
        "alunos": ["Bruno", "Camila", "Daniel", "Fernanda"],
        "nota": 8.5
    }
    # Passa as variáveis para o arquivo 'exercicios.html'
    return render_template('exercicios.html', **dados_teste)


# Rota da Atividade 5 - Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_digitado = request.form.get('usuario')
        senha_digitada = request.form.get('senha')

        # -------------------------------------------------------------
        # CONFIGURAÇÃO DE ACESSO
        # -------------------------------------------------------------
        SEU_NOME = 'marcelo'
        SUA_MATRICULA = '22400362'
 
        if usuario_digitado == SEU_NOME and senha_digitada == SUA_MATRICULA:
            return f"<h1>Bem-vindo ao sistema, {usuario_digitado}!</h1>"
        else:
            # Recarrega a página mostrando uma mensagem de erro
            return render_template('login.html', erro="Login inválido. Verifique seu nome e matrícula.")
 
    return render_template('login.html')


if __name__ == "__main__":
    # Roda o aplicativo em modo de depuração (debug)
    app.run(debug=True)
