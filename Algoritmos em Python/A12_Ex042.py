# Desafio 042 - ler se é triangulo e de que tipo é esclaeno, isosceles ou equilatero

s1 = float(input('Digite o primeiro segmento: '))
s2 = float(input('Digite o segundo segmento: '))
s3 = float(input('Digite o terceiro segmento: '))

if s1 + s2 > s3 and s1 + s3 > s2 and s2 + s3 > s1:
    print('É possível formar triângulo')
    if s1 != s2 and s1 != s3 and s2 != s3:
        print('Além disso, seu triângulo é escaleno.')
    elif (s1 == s2 and s1 != s3 and s2 != s3) or (s1 == s3 and s1 != s2 and s2 != s3) or (s2 == s3 and s2 != s1 and s3 != s1):
        print('Além disso, seu triângulo é isósceles.')
    elif s1 == s2 == s3:
        print('Além disso, seu triângulo é equilátero.')
else:
    print('Não é possível formar triângulo.')
