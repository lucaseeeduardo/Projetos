def fibonacci(quantidade):
    i = 0
    a = 0
    f = 1
    while True :
        if i == quantidade:
            break
        print(a, end=' ')
        i+=1
        if i == quantidade:
            break
        print(f, end=' ')
        i+=1

        a = f
        f = a + f
fibonacci(6)