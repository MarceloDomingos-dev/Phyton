import math
from flask import render_template, request # type: ignore


def calcular():
    etapas = ''
    resultados = ''

    if request.method == 'GET':
        return render_template('calculadora.html', etapas=etapas, resultados=resultados)

    try:
        num1 = float(request.form['num1'])
        operacao = request.form['operacao']

        if operacao == 'sqrt':
            if num1 < 0:
                resultados = 'Erro: número negativo'
                etapas = f'Não existe raiz real de {num1}.'
            else:
                resultados = math.sqrt(num1)
                etapas = f'√{num1} = {resultados}'

        elif operacao == 'log':
            if num1 <= 0:
                resultados = 'Erro: número inválido para logaritmo'
                etapas = f'Não existe logaritmo real de {num1}, pois o número deve ser maior que zero.'
            else:
                resultados = math.log10(num1)
                etapas = f'log({num1}) = {resultados}'

        else:
            num2_valor = request.form.get('num2', '').strip()

            if not num2_valor:
                return render_template(
                    'calculadora.html',
                    etapas='Informe o segundo número para esta operação.',
                    resultados='',
                )

            num2 = float(num2_valor)

            if operacao == '+':
                resultados = num1 + num2
                etapas = f'{num1} + {num2} = {resultados}'

            elif operacao == '-':
                resultados = num1 - num2
                etapas = f'{num1} - {num2} = {resultados}'

            elif operacao == '*':
                resultados = num1 * num2
                etapas = f'{num1} × {num2} = {resultados}'

            elif operacao == '/':
                if num2 == 0:
                    resultados = 'Erro: divisão por zero'
                    etapas = f'Não é possível dividir {num1} por zero.'
                else:
                    resultados = num1 / num2
                    etapas = f'{num1} ÷ {num2} = {resultados}'

            elif operacao == '**':
                resultados = num1 ** num2
                etapas = f'{num1} ^ {num2} = {resultados}'

            else:
                resultados = 'Erro: operação inválida'
                etapas = 'Escolha uma operação válida.'

    except ValueError:
        resultados = 'Erro: valor inválido'
        etapas = 'Digite apenas números válidos nos campos.'

    return render_template('calculadora.html', etapas=etapas, resultados=resultados)
