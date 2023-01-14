# Desafio 046: contagem regressiva com pausa de 1 segundo entre os números
from time import sleep
for c in range(10, -1, -1):
    print(c)
    sleep(1)
print('FELIZ ANO NOVO', '!'*20)
