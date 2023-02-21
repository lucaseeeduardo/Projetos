from random import randint
lista = list()


def sorteio():
    print('Sorteando 5 valores da lista:', end=' ')
    for c in range(0, 6):
        val = randint(0, 9)
        print(val, end=' ')
        lista.append(val)
    print('Pronto!')


def somapar():
    soma = 0
    for p in lista:
        if p % 2 == 0:
            soma = soma + p
    print(f'Somando os valores pares de {lista}, temos: {soma}')


sorteio()
somapar()
