# ler 7 números e separar em par e impar
# num = list()
# lista_pares = list()
# lista_impares = list()
#
# for c in range(0, 7):
#     num.append(int(input(f'Digite o {c+1}º número: ')))
#     if num[c] % 2 == 0:
#         lista_pares.append(num[c])
#     else:
#         lista_impares.append(num[c])
# lista_impares.sort()
# lista_pares.sort()
# num.sort()
# print(f'A lista total foi: {num}')
# print(f'Os valores pares são: {lista_pares}')
# print(f'Os valores ímpares são: {lista_impares}')

# meu código deu 17 linhas, o do guanabara deu 10 kkk a seguir como ele fez
valores = [[], []]
for i in range(1, 8):
    val = int(input(f'Digite o {i}o número: '))
    if val % 2 == 0:
        valores[0].append(val)
    else:
        valores[1].append(val)
valores[0].sort()
valores[1].sort()
print(f'Lista de pares: {valores[0]}')
print(f'Lista de ímpares: {valores[1]}')
