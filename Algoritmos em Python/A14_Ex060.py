# Desafio 060: número e fatorial dele por for e while
# primeiro for e segundo while

num = int(input('Digite o número que deseja saber o fatorial: '))
mult_fat = 1
# num x num-1 x num-2 x num-3 ... num-num
for c in range(num, 0, -1):
    fat = num - (num - c)
    mult_fat = mult_fat * fat
    print(fat, end='')
    print(' x ' if c > 1 else ' = ', end='')
print(mult_fat)
print(f'O fatorial de {num} é {mult_fat}')

# while agora
n = int(input('Número: '))
fn = 1
while n > 0:
    print(n, end='')
    print(' x ' if n > 1 else ' = ', end='')
    fn = fn * n
    n = n - 1
print(fn)
