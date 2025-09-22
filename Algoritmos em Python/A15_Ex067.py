# Tabuada de qualquer número
num = int(input('Quer ver a tabuada de qual valor? '))
print('-'*35)
while True:
    for c in range(1, 11):
        print(f'{num} x {c:2} = {num*c}')
    print('-' * 35)
    num = int(input('Quer ver a tabuada de qual valor? '))
    print('-'*35)
    if num < 0:
        break
