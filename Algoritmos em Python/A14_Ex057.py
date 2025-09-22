# Desafio 057: ler o sexo de uma pessoa que só aceita M ou F até ter a string correta
s = 'M'
while s == 'F' or s == 'M':
    s = str(input('Digite seu sexo [M/F]: ')).strip().upper()
    while s != 'F' and s != 'M':
        print('A sua resposta não está de acordo com o comando solicitado, faça novamente.')
        s = str(input('Digite seu sexo [M/F]: ')).strip().upper()
