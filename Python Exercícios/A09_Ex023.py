# Desafio 023 - digitar um número de 0 até 9999 e fazer com que ele mostre as unidades.

# Essa é com string (1 de 3)

num = str(input('Digite um número: '))

print('Milhar: ', num[0])
print('Centena:', num[1])
print('Dezena: ', num[2])
print('Undiade:', num[3])

# Abaixo é com número (2 de 3)

num2 = str(input('Digite um número: '))
m = num2[:1]
c = num2[1:2]
d = num2[2:3]
u = num2[3:4]

print('Milhar:', m)
print('Centena:', c)
print('Dezena:', d)
print('Unidade:', u)

# Abaixo é com lógica (3 de 3)

num3 = int(input('Digite um número: '))

m1 = num3 // 1000 % 10
c1 = num3 // 100 % 10
d1 = num3 // 10 % 10
u1 = num3 // 1 % 10

print('Milhar: ', m1)
print('Centena: ', c1)
print('Dezena: ', d1)
print('Unidade: ', u1)

# ou assim

n = int(input('Informe um número inteiro: '))

print(f'Analisando o número: {n}')
print(f'Unidade: {n // 1 % 10}')
print(f'Dezena: {n // 10 % 10}')
print(f'Centena: {n // 100 % 10}')
print(f'Milhar: {n // 1000 % 10}')
# 384 % 10 = resto 4 == unidade
# 384 // 10 (para pegar a parte inteira da divisão) = 38(que é a parte inteira % 10 = 3,8
# (resto vai ser igual a 8), então temos que dezena = 8
# 384 // 100 = 3,84, o resto inteiro é 3!
# 3 % 10 = 0,3 = 3!, como é um número com somente 3 algarismos, a divisão inteira já me fornece
# o algarismo da centena, mas se fosse 1354, por exemplo, a divisão inteira seria 13! então tem que sempre seguir
# o script certinho.