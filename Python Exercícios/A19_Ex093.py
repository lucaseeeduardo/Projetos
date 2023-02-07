# o cerne do desafio é colocar lista dentro de dict

banco = dict()
banco['nome'] = str(input('Nome do Jogador: '))
banco['gols'] = list()
banco['partidas'] = int(input(f'Quantas partidas {banco["nome"]} jogou? '))
soma = 0
for c in range(1, banco['partidas']+1):
    gols = int(input(f'Quantos gols na partida {c}?'))
    banco['gols'].append(gols)
    soma = soma + gols
banco['total'] = soma
print(banco)
for k, v in banco.items():
    print(f'O campo {k} tem o valor {v}')
print(f'O jogador {banco["nome"]} jogou {banco["partidas"]} partidas')
for i, n in enumerate(banco['gols']):
    print(f'Na partida {i+1}, fez {n} gols.')
print(f'Foi um total de {sum(banco["gols"])} gols.')
