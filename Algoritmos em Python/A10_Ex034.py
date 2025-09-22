# Desafio 034: aumento de 15% no salario até 9000, acima de 9000 é 10%

s1 = float(input('Informe seu salário: R$'))

if s1 < 1250:
    print('Seu salário agora é de R$ {:.2f}!'.format(s1*1.15))
else:
    print('Seu salário agora é de R$ {:.2f}!'.format(s1*1.10))
