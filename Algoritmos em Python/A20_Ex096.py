# usar def pra fazer calculo de area
def area():
    print('Controle de Terreno')
    print('-' * 20)
    lar = float(input('Largura (m): '))
    comp = float(input('Comprimento (m): '))
    print(f'A área de um terreno de {lar:.1f}x{comp:.1f} é de {lar*comp:.1f}m²')


area()
## eu fiz da forma acima. Abaixo está a forma que o professor resolve
def ar(la, co):
    a = la*co
    print(f'A área de um terreno de {la:.1f}x{co:.1f} é de {a:.1f}m²')


la = float(input('Largura (m): '))
co = float(input('Comprimento (m): '))
ar(la, co)
# tem uma coisa interessante: posso nomear as variáveis da def e dos argumentos que
# são declarados após a def de forma igual. 