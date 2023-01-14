Algoritmo "Ex. 5 - Números superiores à média"

Var

n1, n2, OPCAO: REAL

Inicio
      ESCREVA("Digite o número 1: ")
      LEIA(n1)
      ESCREVA("Digite o número 2: ")
      LEIA(n2)
      ESCREVAL("O QUE DESEJA REALIZAR?")
      ESCREVAL("1 – Adição, 2 – Subtração, 3 – Multiplicação, 4 – Divisão: ")
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
            ESCREVA("Divisão por zero dará erro!")
            FIMALGORITMO
         FIMSE
         ESCREVA(n1, "/", n2," = ", n1/n2)
      FIMSE
      
Fimalgoritmo