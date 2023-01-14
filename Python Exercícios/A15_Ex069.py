# CADASTRO DE PESSOAS IDADE, SEXO, TOTAL MAIS DE 18, QTD HOMENS, QTD MULHERES <20 anos
cont18 = 0
contmasc = 0
contfem = 0

while True:
    print('-'*30)
    print('CADASTRE UMA PESSOA')
    print('-'*30)
    idade = int(input('Idade: '))
    sexo = str(input('Sexo [M/F]: ')).strip().upper()
    while sexo not in "MF":
        sexo = str(input('Sexo [M/F]: ')).strip().upper()
    if idade > 18:
        cont18 = cont18 + 1
    if sexo == 'M':
        contmasc = contmasc + 1
    if sexo == 'F' and idade < 20:
        contfem = contfem + 1
    ask = str(input('***Quer continuar? [S/N]: ')).strip().upper()
    if ask == 'N':
        break
    while ask not in 'SN':
        ask = str(input('***Quer continuar? [S/N]: ')).strip().upper()
        if ask == 'N':
            break
print('FIM DO PROGRAMA')
print(f'Total de pessoas com mais de 18 anos: {cont18}')
print(f'Ao todo temos {contmasc} homens cadastrados.')
print(f'E temos {contfem} mulheres com menos de 20 anos.')
