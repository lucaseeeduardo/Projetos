# Desafio 036: valor, salário e tempo de financiamento + valor parcelas < 30% do salário
# valor ele pode digitar
# salário ele pode digitar
# tempo de financiamento ele pode digitar
# prestação mensal: if não comprometer else comprometer
# prestação = (valor total/tempo)
#
v = float(input('Insira o valor da casa que deseja comprar: '))
s = float(input('Insira o seu salário (mensal): '))
t = float(input('Insira o tempo de financiamento (anos): '))

prestacao = (v / t)/12

if prestacao <= (0.3*s):
    print('Você está aprovado para financiar a casa!')
else:
    print('Infelizmente não é possível para você financiar a casa, pois a prestação'
          f' de R$ {prestacao:.2f} excede R${s*0.3:.2f}, que é 30% do seu salário.')
    print('Com 30% do seu salário e no mesmo tempo de financiamento, você\n'
          f'poderia comprar uma casa de R$ {(s*0.3)*(t*12)}, ou aumentar o\n'
          f'número de prestações desta que deseja para {v/(s*0.3*12):.3f} anos.')
