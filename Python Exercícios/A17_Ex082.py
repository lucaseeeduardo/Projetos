# LISTA DE NUMEROS, LISTA DE PARES E LISTA DE IMPARES
lista = []
impares = []
pares = []
i = 0

while True:
    lista.append(int(input('Digite um número: ')))
    resp = str(input('Quer continuar? [S/N]: '))

    while True:
        if lista[i] % 2 == 0:
            pares.append(lista[i])
        else:
            impares.append(lista[i])
        break

    if resp in 'Nn':
        break
    i += 1

pares.sort()
impares.sort()
lista.sort()

print(f'A lista completa é: {lista}')
print(f'A lista de pares é: {pares}')
print(f'A lista de ímpares é: {impares}')
