
def cadastrar():
    nome = input('Digite seu nome: ')
    idade = input('Digite sua idade: ')
    arquivo = open('ex115\\ex115.txt', 'a')
    arquivo.write(f'{nome} \t\t\t\t\t\t\t {idade} anos\n')
    arquivo.close()

def listar():
    arquivo = open('ex115\\ex115.txt', 'r')
    print(arquivo.read())
    arquivo.close()

def menu():
    print('-'*40)
    print('Menu Principal')
    print('-'*40)
    print('1 - Ver pessoas cadastradas')
    print('2 - Cadastrar nova pessoa')
    print('3 - Sair do sistema')
    print('-'*40)

    while True:
        escolha = int(input('Quero: '))
        if escolha == 1:
            listar()
        elif escolha == 2:
            cadastrar()
        elif escolha != 3:
            print('Não existe essa opção, tente novamente.')
        else:
            break

menu()