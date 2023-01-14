# SORTEAR NÚMEROS e colocá-los em uma tupla
from random import randint
numeros = (randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10),
           randint(1, 10))
print('Os valores sorteados foram: ', end='')
for n in numeros:
    print(n, end=' ')
print(f'\nO maior valor da tupla é: {max(numeros)}')
print(f'O menor valor da tupla é: {min(numeros)}')
