# Desafio 029: crie um programa que leia a velocidade e se ele ultrapassar
# 80Km/h, multado. Multa de R$ 7,00 por cada km acima do limite.

vel = int(input('Digite a velocidade que você passou pelo radar: '))

if vel > 80:
    print('Você foi multado, passou a {}km/h e deverá\n'
          'pagar R${}.'.format(vel, 7*(vel-80)))
else:
    print('Parabéns, você não foi multado e é\n'
          'um motorista consciente!')
