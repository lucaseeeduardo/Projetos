# no exercício ele não pede diferença entre masc e fem, nem usa as
# duas condições de aposentadoria -> acima de 60 e + 35 carteira assinada
from datetime import datetime
dados = dict()
dados['nome'] = str(input('Nome: '))
data = int(input('Ano de Nascimento: '))
dados['idade'] = datetime.today().year - data
dados['ctps'] = int(input('Carteira de Trabalho (0 não tem): '))
if dados['ctps'] != 0:
    dados['contratação'] = int(input('Ano Contratação: '))
    dados['salário'] = float(input('Salário: R$ '))
contribuicao = datetime.today().year - dados['contratação']
# para calcular com qual idade ela vai se aposentar, tem que pensar em dois casos:
# contratacao + 35
# data + 60
# data + 60 - contratacao
aposentadoria = data + 60 - dados['contratação']
if aposentadoria >= 35:
    dados['aposentadoria'] = 60
else:
    dados['aposentadoria'] = dados['contratação'] + 35 - data
for k, v in dados.items():
    print(f'- {k} tem o valor {v}')
