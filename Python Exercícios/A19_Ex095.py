# o exercício é basicamente: [{[]}] lista dentro de dict dentro de lista
banco = list()
jogador = dict()
escolha = 's'
escolhadados = 0
while escolha in 'Ss':
    jogador['nome'] = str(input('Nome do Jogador: '))
    partidas = int(input(f'Quantas partidas {jogador["nome"]} jogou? '))
    jogador['gols'] = list()
    for jogo in range(0, partidas):
        gol = int(input(f'Quantos gols na partida {jogo+1}? '))
        jogador['gols'].append(gol)
    jogador['total'] = sum(jogador['gols'])
    escolha = str(input('Quer continuar? [S/N] '))
    banco.append(jogador.copy())
print('Cód', end='  ')
for k in banco[0]:
    print(f'{k:<15}', end='')
print()
for k, v in enumerate(banco):
    print(f'{k:^5}', end='')
    for d in v.values():
        print(f'{str(d):<15}', end='')
    print()
# banco = [{'nome': lucas, 'gols': [1, 2, 3], 'total':6}, {}]
while escolhadados != 999:
    escolhadados = int(input('Mostrar dados de qual jogador? (999 para parar) '))
    if escolhadados == 999:
        break
    print(f'LEVANTAMENTO DO JOGADOR {banco[escolhadados]["nome"]}')
    for k in range(0, len(banco[escolhadados]['gols'])):
        print(f'No jogo {k+1} fez {banco[escolhadados]["gols"][k]} gols.')
