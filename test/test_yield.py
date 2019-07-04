# fab


def fab(max_num):
    n, a, b = 0, 0, 1
    while n < max_num:
        yield b
        a, b = b, a + b
        n = n + 1


for n in fab(5):
    print(n)

for n in fab(5):
    print(n)
