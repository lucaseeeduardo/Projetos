Algoritmo "Ex. 7 - Sal�rio e imposto"

Var

SALARIO, SALARIOLIQUIDO, IR, INSS, SINDICATO: REAL
Inicio
      ESCREVA("Digite o seu sal�rio bruto: ")
      LEIA(SALARIO)
      ESCREVAL("Sal�rio Bruto      : R$", SALARIO)
      IR <- SALARIO*0.15
      ESCREVAL("(-)IR(15%)         : R$", IR)
      INSS <- SALARIO*0.11
      ESCREVAL("(-)INSS(11%)       : R$", INSS)
      SINDICATO <- SALARIO*0.03
      ESCREVAL("(-)Sidicato(3%)    : R$", SINDICATO)
      SALARIOLIQUIDO <- SALARIO - IR - INSS - SINDICATO
      ESCREVAL("Sal�rio l�quido    : R$", SALARIOLIQUIDO)
Fimalgoritmo