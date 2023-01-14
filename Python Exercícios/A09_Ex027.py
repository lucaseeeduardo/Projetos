# Desafio 027 - nome completo da pessoa - achar primeiro e último nome!

nome = str(input('Digite seu nome completo: '))
nom1 = nome.split()

print(nom1)
print('Seu primeiro nome é {} enquanto seu último nome é {}!'
      .format(nom1[0], nom1[(len(nom1) - 1)]))

# pode ser assim também:
nome = str(input('Digite seu nome completo: ')).strip()

print('Muito prazer em te conhecer!')
print(f'Seu primeiro nome é {nome.split()[0]}.')
print(f'Seu último nome é {nome.split()[len(nome.split())-1]}.')

# interessantes saber: a função split e a função desempenhada pelos colchetes, são referentes a
# nomenclatura de POSIÇÃO. Ou seja, pode ocorrer posição ZERO.
# No entanto, a função len() não avalia posição, mas sim quantidade de caracteres, portanto
# ela não começa no zero, mas sim no 1! ex: 1, 2, 3 caracteres pelo len()
# mas posição 0, 1, 2, 3 e 4 pelo split e pelo colchetes!
