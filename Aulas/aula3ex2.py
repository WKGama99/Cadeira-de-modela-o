import math

a = 0.0001
b = 10000
c = 0.0001 


def equação_padrao(a, b, c):
    delta =b**2 - 4 * a * c
    x1 = (-b + math.sqrt(delta)) / (2 * a)
    x2 = (-b - math.sqrt(delta)) / (2 * a)

    return x1, x2

resultado_d = equação_padrao(a, b, c)

print(f"Resultados: {resultado_d}")