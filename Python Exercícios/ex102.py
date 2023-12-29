def fatorial(num, show=False):
    if(num > 1):
        if(show):
            print(f'{num} x ', end='')
        return num * fatorial(num-1, show)
    else:
        if(show):
            print(f'1 = ', end='')
        return 1

print(fatorial(5, True))