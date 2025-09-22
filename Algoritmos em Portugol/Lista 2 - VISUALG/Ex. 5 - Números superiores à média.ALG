Algoritmo "Ex. 5 - Números superiores à média"

Var

v1, v2, v3, v4, v5: INTEIRO
media :REAL

Inicio
      ESCREVA("Digite o valor 1: ")
      LEIA(v1)
      ESCREVA("Digite o valor 2: ")
      LEIA(v2)
      ESCREVA("Digite o valor 3: ")
      LEIA(v3)
      ESCREVA("Digite o valor 4: ")
      LEIA(v4)
      ESCREVA("Digite o valor 5: ")
      LEIA(v5)
      media <- (v1+v2+v3+v4+v5)/5
      ESCREVAL("A média foi: ", media, ".")
      ESCREVAL("Os valores que superaram a média foram: ")
      SE v1>media ENTAO
         ESCREVAL("V1: ", v1)
      FIMSE
      SE v2>media ENTAO
         ESCREVAL("V2: ", v2)
      FIMSE
      SE v3>media ENTAO
         ESCREVAL("V3: ", v3)
      FIMSE
      SE v4>media ENTAO
         ESCREVAL("V4: ", v4)
      FIMSE
      SE v5>media ENTAO
         ESCREVAL("V5: ", v5)
      FIMSE

Fimalgoritmo