# Exercício 81  digitar n valores, colocar em ordem decrescente e ver se o 5 faz parte da lista
resp = 'S'
i = 0
lista = []
while ('N' not in resp):
    i += 1
    lista.append(int(input('Digite um número: ')))
    resp = str(input('Quer continuar? [S/N]: '))
    if resp == 'n':
        break
lista.reverse()
print(f'A lista em ordem decrescente é: {lista}')
if 5 in lista:
    print('O valor 5 está na lista!')
else:
    print('O valor 5 não está na lista!')
print(f'Você digitou {i} elementos.')
# uma maneira melhor de fazer seria "while True" e dps " if resp not in 'Nn' "