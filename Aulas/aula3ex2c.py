import math 

def resolve_equações(a, b, c):
    delta = b**2 - 4 * a * c 
    raiz = math.sqrt(delta)

    if b >= 0:
        x1 = (-b - raiz) / (2 * a)
        x2 = (2 * c) / (-b - raiz) 
        
    else:
        x1 = (-b + raiz) / (2 * a)
        x2 = (2 * c) / (-b + raiz)

    return x1, x2
    
a = 0.0001
b = 10000
c = 0.0001
     
resultado = resolve_equações(a, b, c)

print("As soluções exatas são:", resultado)