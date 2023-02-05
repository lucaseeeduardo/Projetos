# nome, média e situação (aprovado/reprovado)
dados = dict()
dados['Nome'] = str(input('Digite seu nome: '))
dados['Média'] = float(input('Digite sua média: '))
dados['Situação'] = 'Aprovado'
if dados['Média'] < 7:
    dados['Situação'] = 'Reprovado'
for k, v in dados.items():
    print(f'{k} é igual a {v}')
