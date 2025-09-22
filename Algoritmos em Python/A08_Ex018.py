# Desafio 18 - Fazer um código que apresente o sen, cos e tang de um ângulo.

from math import radians, sin, cos, tan

ang = float(input('Digite o valor do ângulo que você deseja saber '
                  'o cosseno, o seno e a tangente: '))

s = sin(radians(ang))
c = cos(radians(ang))
t = tan(radians(ang))

print('O seno de {:.2f}º é {:.2f} \n'
      'O cosseno de {:.2f}º é {:.2f} \n'
      'A tangente de {:.2f}º é {:.2f} \n'.format(ang, s, ang, c, ang, t))

# outra forma

a = float(input('Digite o ângulo que você deseja saber o valor: '))

print(f'O valor de seno de {a} é {sin(radians(a)):.2f}')
print(f'O valor de cosseno de {a} é {cos(radians(a)):.2f}')
print(f'O valor de tangente de {a} é {tan(radians(a)):.2f}')
