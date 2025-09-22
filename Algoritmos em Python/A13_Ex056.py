# Desafio 056: ler nome, idade e sexo de 4 pessoas e dizer homem mais velho, menores de 20 e media de idade

maisvelhom = 0
maisnovom = 0
count_feminino = 0
count_idade = 0
nome_maisvelhom = ''

for c in range(1, 5):
    print(f'---- {c}ª Pessoa ----')
    nome = str(input('Nome: ')).strip().capitalize()
    idade = int(input('Idade: '))
    sexo = str(input('Sexo [M/F]: ')).strip().upper()
    count_idade = count_idade + idade

    if sexo == 'F' and idade < 20:
        count_feminino = count_feminino + 1

    if sexo == 'M':
        if c == 1:
            maisvelhom = idade
            maisnovom = idade
            nome_maisvelhom = nome
        else:
            if idade > maisvelhom:
                maisvelhom = idade
                nome_maisvelhom = nome
            if idade < maisnovom:
                maisnovom = idade

print(f'A média de idade do grupo é de {count_idade/4} anos.')
print(f'O homem mais velho tem {maisvelhom} anos e se chama {nome_maisvelhom}.')
print(f'Ao todo são {count_feminino} mulheres menores de 20 anos')
