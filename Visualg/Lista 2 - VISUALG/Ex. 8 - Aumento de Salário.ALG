Algoritmo "Ex. 8 - Empresa XYZ"
 //nome do funcion�rio
 //% de aumento
 //sal�rio atual
 // novo sal�rio
Var

SALARIO, NOVOSALARIO, aumento: REAL
NOME :CARACTERE
Inicio
      ESCREVA("Digite o seu nome: ")
      LEIA(NOME)
      ESCREVA("Digite o seu sal�rio atual: ")
      LEIA(SALARIO)

      SE (SALARIO <= 400) ENTAO
         NOVOSALARIO <- SALARIO*1.15
         aumento <- 15
      FIMSE

      SE (SALARIO > 400) E (SALARIO <=700) ENTAO
         NOVOSALARIO <- SALARIO*1.12
         aumento <- 12
      FIMSE

      SE (SALARIO > 700) E (SALARIO <=1000) ENTAO
         NOVOSALARIO <- SALARIO*1.10
         aumento <- 10
      FIMSE

      SE (SALARIO > 1000) E (SALARIO <=1800) ENTAO
         NOVOSALARIO <- SALARIO*1.07
         aumento <- 7
      FIMSE

      SE (SALARIO > 1800) E (SALARIO <=2500) ENTAO
         NOVOSALARIO <- SALARIO*1.04
         aumento <- 4
      FIMSE
      
      SE (SALARIO <= 2500) ENTAO
         ESCREVAL("Prezado ", NOME, ", seu sal�rio teve aumento.")
         ESCREVAL("Voc� ganha", SALARIO," e passar� a ganhar ", NOVOSALARIO)
         ESCREVAL("Isso significa um aumento de ", aumento, "%.")
      SENAO
         ESCREVA("Voc� n�o teve aumento de sal�rio.")
      FIMSE
      
Fimalgoritmo