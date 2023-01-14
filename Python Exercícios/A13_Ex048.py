# Desafio 048: soma entre todos os números ímpares entre 1 e 500 que são múltiplos de 3

s = 0
cont = 0
for c in range(0, 501):
    if c % 3 == 0 and c % 2 != 0:
        print(c)
        cont = cont + 1
        s = s + c
        print('\033[32m', s, '\033[m')
        print(' ', '\033[31m', cont, '\033[m')

# existe a forma um pouquinho mais simplificada:

s = 0
cont = 0
for n in range(1, 501, 2):
    if n % 3 == 0:
        s = s + n
        cont = cont + 1
        print(n, end=' ')
print(' ')
print(s)
print(cont)
