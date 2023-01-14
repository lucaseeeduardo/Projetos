palavras = ('Aprender', 'Programar', 'Linguagem', 'Python', 'Curso')
for verbo in palavras:
    print('\n',verbo, end=' ')
    for letra in verbo:
        if letra.lower() in 'aeiou':
            print(letra, end=' ')
