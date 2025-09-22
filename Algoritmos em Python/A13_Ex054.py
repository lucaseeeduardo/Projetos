# Desafio 054: analisar 7 datas de nasc e ver qm é mais velho/maior de idade e menor
from datetime import date

ano_atual = date.today().year
cont18 = 0
cont_menor = 0
for c in range(1, 8):
    data = int(input(f'Em que ano a {c}ª pessoa nasceu? '))
    if (ano_atual - data) < 18:
        cont_menor = cont_menor + 1
    else:
        cont18 = cont18 + 1
print(f'Ao todo tivemos {cont18} pessoas maiores de idade.')
print(f'E também tivemos {cont_menor} pessoas menores de idade.')
