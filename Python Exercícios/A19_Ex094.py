# fazer um cadstro com dict dentro de lista
cadastro = dict()
banco = list()
validacao = 's'
while validacao not in 'nN':
    cadastro['nome'] = str(input('Nome: '))
    cadastro['sexo'] = str(input('Sexo [M/F]: '))
    while cadastro['sexo'] not in 'Mm' and cadastro['sexo'] not in 'Ff':
        print('ERRO! Por favor, digite apenas M ou F.')
        cadastro['sexo'] = str(input('Sexo [M/F]: '))
    cadastro['idade'] = int(input('Idade: '))
    banco.append(cadastro.copy())
    validacao = str(input('Quer continuar? [S/N] '))
    while validacao not in 'sS' and validacao not in 'Nn':
        print('ERRO! Responda apenas S ou N.')
        validacao = str(input('Quer continuar? [S/N] '))
print(f'A) Ao todo temos {len(banco)} pessoas cadastradas.')
print(f'B) A média de idade é de {} anos')
print(f'C) Mulheres cadastradas')
print(f'D) Lista de pessoas acima da média: ')
