# tenho que fazer um código que faça aparecer a palavra TRUE ou FALSE para c= ((A < B) || (A + B==10))
.data
	entrada1: .asciiz "Digite A: "
	entrada2: .asciiz "Digite B: "
	false: .asciiz "\nFALSE"
	true: .asciiz "\nTRUE"
.text
	la $a0, entrada1 # colocando o endereço da entrada 1 em $a0
	li $v0, 4 # printando entrada 1
	syscall

	li $v0, 5 # usuário digita número A
	syscall 
	move $t1, $v0 # movendo para $t1 o valor de entrada 1

	la $a0, entrada2 # printando entrada 2
	li $v0, 4
	syscall

	li $v0, 5 # usuário digita número B
	syscall

	move $t2, $v0 # movendo para $t2 o valor de entrada2
	add $t3, $t1, $t2 # somando e colocando em $t3 a soma 

	## aqui preciso dividir as duas condições - se termo 1 verdadeiro ou termo 2 verdadeiro, um registrador receberá 1 

	seq $t4, $t3, 10 # se a soma for igual a 10 (A + B == 10), então o número 1 será alocado em $t4
	slt $t5, $t1, $t2 ## se A < B, então 1 é alocado em $t5
	or $t6, $t5, $t4 ## se A < B => 1 ou A + B == 10 =>1, então $t6 será 1, se não será 0
	bnez $t6, setrue # se $t6 não for zero, ou seja, se for 1, então pula pra label "setrue", caso contrário, continua.
	la $a0, false # como $t6 == 0, então $a0 carrega o endereço da label false
	li $v0, 4 # v0 printa o conteúdo da label false, que é "\nFALSE"
	syscall

	li $v0, 10
	syscall

	setrue:
		la $a0, true # carregando para a0 o endereço de true
		li $v0, 4  # printando o conteúdo do endereço de a0, que é "\nTRUE"
		syscall