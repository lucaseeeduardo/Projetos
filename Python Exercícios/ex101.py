
def voto(anoNascimento):
    from datetime import date
    idade = date.today().year - anoNascimento
    print(f"Sua idade é: {idade}")
    if(idade<16):
        print("NEGADO")
    elif(idade<18):
        print("OPCIONAL")
    elif(idade<65):
        print("OBRIGATÓRIO")
    elif(idade>=65):
        print("OPCIONAL")

voto(2000)
voto(2005)
voto(2007)
voto(2010)
voto(1959)
voto(1930)
voto(1958)