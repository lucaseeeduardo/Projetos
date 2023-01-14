# criar um contador de parênteses para validar expressões matemáticas
# pe = parênteses esquerda ; pd  = parênteses direita
# o que eu fiz antes de ver a resolução tem um erro em que se começar com ) não dá erro, e se tiver a expressão toda esquisita, também daria como certo: ())(
exp = str(input('Digite a expressão: '))

esquerda = exp.count('(')
direita = exp.count(')')

if esquerda == direita:
    print(f'A expressão está correta, existem:'
          f'\n{esquerda} parênteses na esquerda'
          f'\n{direita} parênteses na direita')
else:
    print('A expressão está incorreta, existem:'
          f'\n{esquerda} parênteses na esquerda'
          f'\n{direita} parênteses na direita')

# agora parecido com a forma que o guanabara fez:
frase = str(input('Digite uma expressão: '))
lista_simb = []
for simb in frase:
    if simb == '(' or simb == ')':
        lista_simb.append(simb)
    if len(lista_simb) > 0 and lista_simb.count(')') > 0:
        lista_simb.remove('(')
        lista_simb.remove(')')
if len(lista_simb) == 0:
    print('Sua expressão está correta.')
else:
    print('Sua expressão está incorreta.')
print(f'Os seguintes parênteses estão sem pares: {lista_simb}')
