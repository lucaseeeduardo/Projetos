# criar uma tupla com os 20 primeiros colocados, na ordem de colocação,
# mostrar apenas
# a)5 primeiros; b) últimos 4; c)ordem alfabética; d)em que posição está a chapecoense
lista = ('Palmeiras', 'Internacional', 'Flamengo', 'Fluminense', 'Corinthians', 'Athletico-PR', 'Atlético-MG', 'América-MG', 'Fortaleza', 'Botafogo', 'Santos', 'São Paulo', 'Bragantino', 'Goiás', 'Coritiba', 'Ceará SC', 'Cuiabá', 'Atlético-GO', 'Avaí', 'Juventude')
print(lista)
print(f'Os 5 primeiros são: {lista[:5]}')
print(f'Os 4 últimos são: {lista[16:]}')
print(f'Em ordem alfabética fica: {sorted(lista)}')
print(f'A chapecoense está na {lista.index("Palmeiras")+1}ª posição')
