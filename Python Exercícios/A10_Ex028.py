# Desafio 028 - Escreva um programa que informe um número aleatório
# de 1 a 5 que o leitor precisa advinhar, com o computador
# informando se o leitor venceu ou perdeu
import random
from random import randint

print('O computador sorteará um número de 1 a 5 a seguir '
      'e você precisa advinhar qual é: ')
print('Computador: (?)')

nc = random.choice([1, 2, 3, 4, 5])
num1 = int(input('Digite qual número você acha que é: '))

if num1 == nc:
    print('Parabens, você escolheu o mesmo número que o computador: {}!'.format(nc))
else:
    print('Tente outra vez.')
    print('O Computador venceu: {}.'.format(nc))
print('--FIM--')

# ou a maneira que o guanabara fez:
n = int(input('Em que número eu pensei? '))
pc = randint(1, 5)

print('PROCESSANDO...')

if pc == n:
    print('PARABÉNS! Você conseguiu me vencer!')
else:
    print('GANHEI! Eu pensei no número {} e não no {}!'.format(pc, n))

# ou

print('\033[1;32m-=-\033[m'*20)
print('\033[1;34mVou pensar em um número entre 0 e 5. Tente adivinhar...\033[m')
print('\033[1;32m-=-\033[m'*20)

nco = randint(0, 5)
npe = int(input('Em que número eu pensei? '))

if nco == npe:
    print(f'PARABÉNS, você ganhou! Eu realmente pensei {npe}')
else:
    print(f'FAILED, você perdeu, eu pensei em {nco}')
