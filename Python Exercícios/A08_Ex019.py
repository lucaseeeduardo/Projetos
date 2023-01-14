# Desafio 19 - criar um código que sorteie uma entre várias pessoas
import random

a1 = input('Digite o nome do Aluno 1: ')
a2 = input('Digite o nome do Aluno 2: ')
a3 = input('Digite o nome do Aluno 3: ')
a4 = input('Digite o nome do Aluno 4: ')

lista = [a1, a2, a3, a4]
escolhido = random.choice(lista)

print('O aluno escolhido é {}'.format(escolhido))

# ou

print(f'O aluno sorteado foi {random.choice(lista)}!')
