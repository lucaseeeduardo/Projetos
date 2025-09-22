# Desafio - media 5 reprovado, 5 - 6.9 recuperação, >7 aprovado

nota1 = float(input('Digite sua primeira nota: '))
nota2 = float(input('Digite sua segunda nota: '))

m = (nota1+nota2)/2

if m >= 7:
    print('Parabéns, você foi \033[1;32mAPROVADO\033[m!')
elif 5 <= m < 6.9:
    print('Você está em \033[4;33mRECUPERAÇÃO\033[m')
elif m < 5:
    print('Você foi \033[2;31mREPROVADO\033[m')
