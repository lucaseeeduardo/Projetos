# Desafio 038: comparar valores, a maior, b maior ou igual

v1 = float(input('Digite o primeiro valor: '))
v2 = float(input('Digite o segundo valor: '))

if v1 > v2:
    print('\033[31mO primeiro valor é maior.\033[m')
elif v2 > v1:
    print('\033[35mO segundo valor é maior\033[m')
elif v1 == v2:
    print('\033[41mNão existe valor maior, os dois valores são iguais.\033[m')
