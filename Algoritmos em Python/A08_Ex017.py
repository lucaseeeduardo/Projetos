# Desafio 17 - calcular a hipotenusa

from math import sqrt

c1 = float(input('Digite o tamanho de um cateto: '))
c2 = float(input('Digite o tamanho do outro cateto: '))

h = sqrt(pow(c1, 2)+pow(c2, 2))

print('A hipotenusa dos catetos {} e {} é {}'.format(c1, c2, h))
