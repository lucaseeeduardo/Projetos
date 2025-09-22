# Desafio 043: IMC e classificação

peso = float(input('Digite seu peso em kg: '))
altura = float(input('Digite sua altura em metros: '))

imc = peso/pow(altura, 2)  # ou peso/(altura**2)

print(f'Seu IMC é de {imc:.1f}! E: ')

if imc < 18.5:
    print('\033[31mVocê está abaixo do peso!\033[m')

elif 18.5 <= imc < 25:
    print('\033[1;34mSeu peso é ideal!\033[m')

elif 25 <= imc < 30:
    print('Você está em sobrepeso.')

elif 30 <= imc < 40:
    print('Você está obeso.')

elif imc >= 40:
    print('Você apresenta um quadro de obesidade mórbida.')
