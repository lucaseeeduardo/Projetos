Algoritmo "Ex. 7 - Tabela de op��es "

Var

n1, n2, OPCAO: REAL
parouimpar1, parouimpar2 :CARACTERE
Inicio
      ESCREVA("Digite o primeiro n�mero: ")
      LEIA(n1)
      ESCREVA("Digite o segundo n�mero: ")
      LEIA(n2)

      SE (n2 % n1 >= 1) E (n2 % n1 <=4 ) ENTAO
         SE (n2 % n1 = 1) ENTAO // CASO 1
            ESCREVA("SOMA: ", n1+n2+1)
         FIMSE

         SE (n2 % n1 = 2) ENTAO // CASO 2

            SE (n1 % 2 = 0) ENTAO
               parouimpar1 <- "PAR"
            SENAO
               parouimpar1 <- "�MPAR"
            FIMSE

            SE (n2 % 2 = 0) ENTAO
               parouimpar2 <- "PAR"
            SENAO
               parouimpar2 <- "�MPAR"
            FIMSE
            ESCREVA("O primeiro n�mero �", parouimpar1, " e o segundo n�mero �", parouimpar2)
         FIMSE

         SE (n2 % n1 = 3) ENTAO // CASO 3
            ESCREVA("MULTIPLICA��O", (n1+n2)*(n1))
         FIMSE

         SE (n2 % n1 = 4) ENTAO // CASO 4
            SE (n2 <> 0) ENTAO
                ESCREVA("DIVIS�O", (n1+n2)*(n2))
            FIMSE
         FIMSE
      SENAO
           ESCREVA("QUADRADOS: ", n1^2, " e ", n2^2) // CASO 5
      FIMSE
Fimalgoritmo