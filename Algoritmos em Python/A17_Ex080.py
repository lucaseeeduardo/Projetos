# colocar elementos na lista e deixá-la ordenada sem usar sort. O intuito é incluir já em ordem.
lista = []
for c in range(0, 5):
    num = int(input(f'Digite o {c+1}º número: '))
    if c == 0 or num > lista[-1]:
        lista.append(num)
    else:
        pos = 0
        while pos < len(lista):
            if num <= lista[pos]:
                lista.insert(pos, num)
                break
            pos += 1
print(lista)
