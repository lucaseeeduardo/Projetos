# a) soma de pares; b) soma terceira coluna; c) maior valor segunda linha
# aqui eu declarei dessa forma para visualizar melhor
matriz = [[],
          [],
          []]
# NESSE CASO AQUI, 0, 1 e 2 são linhas 0, 1 e 2
listanum = [[], []]
somacol = 0
for LIN in range(0, 3):
    for COL in range(0, 3):
        num = int(input(f'Digite um valor para [{LIN}, {COL}]: '))
        matriz[LIN].append(num)
        if num % 2 == 0:
            listanum[0].append(num)
        else:
            listanum[1].append(num)
for LIN in range(0, 3):
    for COL in range(0, 3):
        print(f'[ {matriz[LIN][COL]} ]', end='')
        if COL == 2:
            somacol = somacol + matriz[LIN][COL]
    print('')
print(f'Os números pares são: {listanum[0]}\n'
      f'Os números ímpares são: {listanum[1]}\n'
      f'A soma dos valores da terceira coluna é: {somacol}\n'
      f'O maior valor da segunda linha é: {max(matriz[1])}')
