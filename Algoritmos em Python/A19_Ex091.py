# 4 jogadores resultados aleatórios, resultados em dicionário, dict em ordem
import random
from operator import itemgetter
jogadores = {'jogador 1': random.randint(1, 6),
             'jogador 2': random.randint(1, 6),
             'jogador 3': random.randint(1, 6),
             'jogador 4': random.randint(1, 6),
             'jogador 5': random.randint(1, 6)}
for k, v in jogadores.items():
    print(f'O {k} tirou {v}')
ranking = sorted(jogadores.items(), key=itemgetter(1), reverse=True)
print(ranking)
for i, v in enumerate(ranking):
    print(f'{i+1}º Lugar: {v[0]} tirou {v[1]}')
