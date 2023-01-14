num = int(input('Digite um número para calcular seu fatorial: '))
n = num
fatorial = 1
print(f'Calculando {num}! → ', end='')
while n > 0:
    print(n, 'x ' if n > 1 else '= ', end='')
    fatorial = fatorial * n
    n = n - 1
print(fatorial)