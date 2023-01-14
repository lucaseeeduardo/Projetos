# Desafio 30 : crie um programa que leia um número e diga se é par ou impar

num = int(input('Digite um número inteiro: '))

if (num % 2) == 1:
    print('O número {} é ímpar!'.format(num))
else:
    print('O número {} é par!'.format(num))

# ou assim

n1 = int(input('\033[1;31mMe diga um número qualquer: \033[m'))

if n1 % 2 == 0:
    print(f'{n1} é par!')
else:
    print(f'{n1} é ímpar!')

