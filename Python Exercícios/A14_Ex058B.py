from random import randint
print('Sou seu computador...')
print('Acabei de pensar em um número entre 0 e 10.')
print('Será que você consegue adivinhar qual foi?')
computador = randint(0, 10)
cont = 1
palpite = int(input('Qual é seu palpite? '))
while palpite != computador:
    cont = cont + 1
    if palpite > computador:
        print('Menos... Tente mais uma vez.')
    elif palpite < computador:
        print('Mais... Tente mais uma vez.')
    else:
        print('Parabéns, você acertou!!')
    palpite = int(input('Qual é seu palpite? '))
print(f'Acertou com {cont} tentativas. Parabéns!')
