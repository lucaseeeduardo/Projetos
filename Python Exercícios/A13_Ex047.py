# Desafio 047: numeros pares de 1 a 50

for c in range(0, 51, 2):
    print(c, end=' ')

# ou assim

print(' ')
for n in range(0, 51):
    if n % 2 == 0:
        print(n, end=' ')
