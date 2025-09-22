# Desafio 031: calcule o valor a pagar com distancia em km. R$ 0,50 a cada km até 200km.
# R$ O,45 por km para km>200

distancia = float(input('Digite a distancia que você percorreu para saber quanto deve pagar: '))

if distancia <= 200:
    print('Você deve pagar R$ {:.2f}!'.format(distancia*0.50))
else:
    print('Você deve pagar R$ {:.2f}!'.format(distancia*0.45))
