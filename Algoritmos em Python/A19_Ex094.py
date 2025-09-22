# fazer um cadstro com dict dentro de lista
cadastro = dict()
banco = list()
validacao = 's'
listamulheres = list()
while validacao not in 'nN':
    cadastro['nome'] = str(input('Nome: '))
    cadastro['sexo'] = str(input('Sexo [M/F]: '))
    while cadastro['sexo'] not in 'Mm' and cadastro['sexo'] not in 'Ff':
        print('ERRO! Por favor, digite apenas M ou F.')
        cadastro['sexo'] = str(input('Sexo [M/F]: '))
    cadastro['idade'] = int(input('Idade: '))
    banco.append(cadastro.copy())
    if cadastro['sexo'] in 'Ff':
        listamulheres.append(cadastro.copy())
    validacao = str(input('Quer continuar? [S/N] '))
    while validacao not in 'sS' and validacao not in 'Nn':
        print('ERRO! Responda apenas S ou N.')
        validacao = str(input('Quer continuar? [S/N] '))
print(f'A) Ao todo temos {len(banco)} pessoas cadastradas.')
isoma = 0
# banco = [{'nome': Lucas, 'sexo': m, 'idade': 10}, {}]
for c in range(0, len(banco)):
    isoma = isoma + banco[c]['idade']

print(f'B) A média de idade é de {isoma/len(banco)} anos')
print(f'C) As mulheres cadastradas foram: ', end='')
for mulheres in range(0, len(listamulheres)):
    print(listamulheres[mulheres]['nome'], end=' ')
print()
print(f'D) Lista de pessoas acima da média: ')
# banco = [{'nome': Lucas, 'sexo': m, 'idade': 10}]
for pessoa in range(0, len(banco)):
    if banco[pessoa]['idade'] > isoma/len(banco):
        for k, v in banco[pessoa].items():
            print(f'{k} = {v};', end=' ')
        print()
