# tenho que fazer um c�digo que fa�a aparecer a palavra TRUE ou FALSE para c= ((A < B) || (A + B==10))
.data
	entrada1: .asciiz "Digite A: "
	entrada2: .asciiz "Digite B: "
	false: .asciiz "\nFALSE"
	true: .asciiz "\nTRUE"
.text
	la $a0, entrada1 # colocando o endere�o da entrada 1 em $a0
	li $v0, 4 # printando entrada 1
	syscall

	li $v0, 5 # usu�rio digita n�mero A
	syscall 
	move $t1, $v0 # movendo para $t1 o valor de entrada 1

	la $a0, entrada2 # printando entrada 2
	li $v0, 4
	syscall

	li $v0, 5 # usu�rio digita n�mero B
	syscall

	move $t2, $v0 # movendo para $t2 o valor de entrada2
	add $t3, $t1, $t2 # somando e colocando em $t3 a soma 

	## aqui preciso dividir as duas condi��es - se termo 1 verdadeiro ou termo 2 verdadeiro, um registrador receber� 1 

	seq $t4, $t3, 10 # se a soma for igual a 10 (A + B == 10), ent�o o n�mero 1 ser� alocado em $t4
	slt $t5, $t1, $t2 ## se A < B, ent�o 1 � alocado em $t5
	or $t6, $t5, $t4 ## se A < B => 1 ou A + B == 10 =>1, ent�o $t6 ser� 1, se n�o ser� 0
	bnez $t6, setrue # se $t6 n�o for zero, ou seja, se for 1, ent�o pula pra label "setrue", caso contr�rio, continua.
	la $a0, false # como $t6 == 0, ent�o $a0 carrega o endere�o da label false
	li $v0, 4 # v0 printa o conte�do da label false, que � "\nFALSE"
	syscall

	li $v0, 10
	syscall

	setrue:
		la $a0, true # carregando para a0 o endere�o de true
		li $v0, 4  # printando o conte�do do endere�o de a0, que � "\nTRUE"
		syscall