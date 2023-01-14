numeros = (int(input('Digite um número: ')),
           int(input('Digite outro número: ')),
           int(input('Digite mais um número: ')),
           int(input('Digite o último número: ')))

print(f'Você digitou os valores: {numeros}')
print(f'O valor 9 apareceu {numeros.count(9)} vezes.')
if 3 not in numeros:
    print(f'O valor 3 não foi digitado em nenhuma posição')
else:
    print(f'O valor 3 foi digitado primeiramente na posição: {numeros.index(3)+1}')

print('Os números pares da tupla foram: ', end='')
for n in numeros:
    if n % 2 == 0:
        print(n, end='')