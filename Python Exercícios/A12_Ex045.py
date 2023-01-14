# Desafio 045 - faça o computador jogar jokenpo com você, pedra papel tesoura
import random

you = str(input('Pedra, papel ou tesoura: ')).upper().strip()

escolhas = ['PEDRA', 'PAPEL', 'TESOURA']
computador = random.choice(escolhas)

print(f'Computador: {computador}')

if computador == 'PEDRA' and you == 'PAPEL':
    print('Parabéns, você ganhou.')

elif computador == 'PEDRA' and you == 'TESOURA':
    print('Você perdeu.')

elif computador == you:
    print('Empatamos.')

elif computador == 'TESOURA' and you == 'PEDRA':
    print('Você ganhou.')

elif computador == 'TESOURA' and you == 'PAPEL':
    print('MWAHAHAAH você perdeu.')

elif computador == 'PAPEL' and you == 'PEDRA':
    print('Você PERDEU.')

elif computador == 'PAPEL' and you == 'TESOURA':
    print('Você ganhou.')
