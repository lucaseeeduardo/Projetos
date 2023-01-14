# PROGRMA QUE JOGA PAR OU IMPAR
import random
cont = 0
contvezes = 0
while True:
    contvezes = contvezes + 1
    valor = int(input('Diga um valor: '))
    if valor < 0:
        print('Escolha apenas números inteiros e maiores que zero. Tente novamente.')
        break
    escolha = ' '
    while escolha not in 'PI':
        escolha = str(input('Par ou Ímpar? [P/I]: ')).strip().upper()[0]
    computador = random.randint(0, 10)
    total = computador + valor

    print(f'Você jogou \033[1;34m{valor}\033[m e o computador \033[1;31m{computador}\033[m.'
          f' Total de \033[1;33m{total}\033[m DEU ', end='')
    print('PAR!' if total % 2 == 0 else 'ÍMPAR!')

    if total % 2 == 0 and escolha == 'P':
        print('Parabéns, você ganhou. Tente novamente...')
    elif total % 2 == 1 and escolha == 'I':
        print('Parabéns, você ganhou. Tente novamente...')
    else:
        print('Você perdeu.')
        break
print(f'Você venceu {cont} vezes das {contvezes} partidas jogadas!')
