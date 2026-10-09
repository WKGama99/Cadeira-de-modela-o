import math
a = 0.0001
b = 10000
c = 0.0001

def resolve_alternativa(a, b, c):
    delta = b**2 - 4 * a * c
    x1 = (2 * c) / (-b -  math.sqrt(delta))
    x2 = (2 * c) / (-b + math.sqrt(delta))
    return x1, x2

resultado_b = resolve_alternativa(a, b, c)
print(f"Resultados: {resultado_b}")