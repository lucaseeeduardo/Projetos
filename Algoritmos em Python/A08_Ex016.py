# Desafio 16 - criar um programa que leia um número real qualquer e só mostre a parte inteira
from math import trunc
n1 = float(input('Digite um número qualquer com casas decimais para saber '
           'sua parte inteira: '))
n2 = trunc(n1)
print('A parte inteira de {} é {}!'.format(n1, n2))

# outra forma

print(f'A parte inteira de {n1} é {n1 // 1:.0f}!')
