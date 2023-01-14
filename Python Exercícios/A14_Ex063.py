# 1 termo =0; 2º termo igual 1; 3º termo igual aos dois anteriores
ts = 1
ta = 0
cont = 0
print('-'*23)
print('SEQUÊNCIA DE FIBONACCI')
print('-'*23)
termos = int(input('Quantos termos você quer mostrar? '))
while cont <= termos:
    print(ta,'→', ts,'PAUSA' if cont == termos else '→ ', end='')
    ta = ta + ts
    ts = ts + ta
    cont = cont + 1
