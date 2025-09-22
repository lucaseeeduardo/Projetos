# Desafio 044 - valor de desconto por modo de pagamento dinheiro, cartao, 2x cartao e 3x cartao

produto = float(input('Digite o valor do produto: '))

print('As formas de pagamento são as seguintes:\n'
      '')
print('1) À vista no dinheiro/cheque com 10% de desconto,\n'
      '2) À vista no cartão com 5% de desconto,\n'
      '3) Em até 2x no cartão com valor normal,\n'
      '4) Em 3x ou mais no cartão.\n'
      '')

pagamento = int(input('Digite a sua forma de pagamento: '))

if pagamento == 1:
    print(f'O valor a ser pago é de R$ {produto*0.9}!')

elif pagamento == 2:
    print(f'O valor a ser pago é de R$ {produto*0.95}!')

elif pagamento == 3:
    print(f'O valor a ser pago é de R$ {produto}')

elif pagamento == 4:
    nparcelas = int(input('Quantas parcelas?'))
    print(f'Sua compra será parcelada em {nparcelas}x de R$ {produto*1.2/nparcelas}')
    print(f'Sua compra de R$ {produto} vai custar R$ {produto*1.2}')
else:
    print('Opção inválida de pagamento, tente novamente.')
