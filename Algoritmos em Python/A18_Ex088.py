# fazer um palpitador da mega sena a) quantos jogos para sortear; b) random 6 numeros de 1 a 60
from random import randint
from time import sleep
jogos = int(input('Digite quantos jogos você quer fazer: '))
for c in range(0, jogos):
    listajogo = list()
    for valores in range(0, 6):
        listajogo.append(randint(1, 60))
    sleep(0.45)
    listajogo.sort()
    print(f'Jogo {c+1}: {listajogo}')
    listajogo.clear()
sleep(0.45)
