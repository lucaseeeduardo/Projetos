# matriz 3x3 fazer e printar
# coluna = COL; linha = LIN
# deixei a matriz declarada dessa forma para auxiliar na visualização
matriz = [[],
          [],
          []]
# NESSE CASO AQUI, 0, 1 e 2 são linhas 0, 1 e 2
for LIN in range(0, 3):
    for COL in range(0, 3):
        matriz[LIN].append(int(input(f'Digite um valor para [{LIN}, {COL}]: ')))
for LIN in range(0, 3):
    for COL in range(0, 3):
        print(f'[ {matriz[LIN][COL]} ]', end='')
    print('')
