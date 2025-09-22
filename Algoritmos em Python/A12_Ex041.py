# Desafio 041 - Ano de nascimento e categoria mirim, infantil, junior, senior, master

from datetime import datetime

nasc = int(input('Digite seu ano de nascimento: '))
hoje = datetime.today().year
idade = hoje - nasc

if idade <= 9:
    print('Sua categoria é MIRIM.')
elif 9 < idade <= 14:
    print('Sua categoria é INFANTIL.')
elif 14 < idade <= 19:
    print('Sua categoria é JUNIOR.')
elif idade == 20:
    print('Sua categoria é SÊNIOR')
elif idade > 20:
    print('Sua categoria é MASTER.')
