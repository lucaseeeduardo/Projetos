d = int(input('Digite o total de dias que alugou o carro: '))
km = float(input('Digite o total de km rodados com o carro: '))

print('O total a pagar é de R$ {:.2f}!'.format((d*60)+(km*0.15)))
