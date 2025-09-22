def pyhelp():
    while True:
        entrada = input('Função ou Biblioteca: ')
        if entrada == 'FIM':
            break
        help(entrada)

pyhelp()
