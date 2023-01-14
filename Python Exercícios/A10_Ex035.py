# Desafio 035: quais tamanhos de segmentos formam um triangulo?

r1 = float(input('Digite o tamanho do primeiro segmento: '))
r2 = float(input('Digite o tamanho do segundo segmento: '))
r3 = float(input('Digite o tamanho do terceiro segmento: '))

if r1 < r2 + r3 and r2 < r1 + r3 and r3 < r1 + r2:
    print('É possível formar triângulo!')
else:
    print('Não é possível formar triângulo')
