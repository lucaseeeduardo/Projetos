Algoritmo "Ex. 5 - N�meros superiores � m�dia"

Var

n1, n2, OPCAO: REAL

Inicio
      ESCREVA("Digite o n�mero 1: ")
      LEIA(n1)
      ESCREVA("Digite o n�mero 2: ")
      LEIA(n2)
      ESCREVAL("O QUE DESEJA REALIZAR?")
      ESCREVAL("1 � Adi��o, 2 � Subtra��o, 3 � Multiplica��o, 4 � Divis�o: ")
      LEIA(OPCAO)
      SE (OPCAO = 1) ENTAO
         ESCREVA(n1, "+", n2," = ", n1+n2)
      FIMSE
      SE (OPCAO = 2) ENTAO
         ESCREVA(n1, "-", n2," = ", n1-n2)
      FIMSE
      SE (OPCAO = 3) ENTAO
         ESCREVA(n1, "X", n2," = ", n1*n2)
      FIMSE
      SE (OPCAO = 4) ENTAO
         SE (n2 = 0) ENTAO
            ESCREVA("Divis�o por zero dar� erro!")
            FIMALGORITMO
         FIMSE
         ESCREVA(n1, "/", n2," = ", n1/n2)
      FIMSE
      
Fimalgoritmo