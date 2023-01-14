# Desafio 052: número inteiro é ou não primo?
num = int(input('Digite qualquer número para saber se é primo: '))
tot = 0
for c in range(1, num + 1):
    if num % c == 0:
        print('\033[34m', end=' ')
        tot = tot + 1
    else:
        print('\033[31m', end=' ')
    print(c, end=' ')
print(' ')
if tot <= 2:
    print(f'\033[33mO total de vezes que o número {num} foi divisível é de: {tot}, e por isso ele é primo')
else:
    print(f'\033[31mO total de vezes que o número {num} foi divisível é de: {tot}, maior que 2, portanto não é primo.')
