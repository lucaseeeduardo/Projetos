# Desafio 039: ainda vai se alistar, já é hora de se alistar, já se alistou
# tempo relativo entre cada variável

from datetime import date
sexo = str(input('Qual seu sexo: ')).upper().strip()

if sexo == 'FEMININO':
    print('O alistamento não é obrigatório para mulheres.')
elif sexo == 'MASCULINO':
    nasc = int(input('Digite o ano de seu nascimento: '))
    ano_atual = date.today().year

    print(f'Quem nasceu em {nasc} tem {ano_atual - nasc} anos em {ano_atual}')

    if (ano_atual - nasc) < 18:
        if 18 - (ano_atual - nasc) == 1:
            print(f'Você faz/fez {ano_atual - nasc} anos neste ano e ainda falta 1 ano para o alistamento.')
        else:
            print(f'Você tem {ano_atual - nasc} anos e ainda faltam {18 - (ano_atual - nasc)} anos para o alistamento.')
    elif (ano_atual - nasc) == 18:
        print(f'Este ano, {ano_atual}, é o ano para você se alistar.')
    elif (ano_atual - nasc) > 18:
        if ano_atual - (nasc+18) == 1:
            print(f'Você se alistou ano passado e neste ano completa/completou 1 ano de alistamento.')
        else:
            print(f'Você se alistou em {nasc + 18}, já fazem {ano_atual-(nasc+18)} anos.')
