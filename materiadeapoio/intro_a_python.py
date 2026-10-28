"""
Sintaxe essencial de Python
Modelação Computacional de Sistemas Físicos

Executar com:
>> python intro_a_python.py
"""

# ----------------------------------------------------------------------
# 1. Variáveis e tipos

# Em Python não se declara o tipo: ele resulta do valor atribuído.
n = 5  # int            — inteiro exato, sem limite de dimensão
x = 2.5  # float        — vírgula flutuante, ~16 dígitos
z = 1 + 2j  # complex   — a unidade imaginária escreve-se 1j
nome = "Terra"  # str   — conjunto de caracteres
existe = True  # boo    — True ou False

# O sinal = é atribuição, não igualdade. Esta linha lê-se
# "calcula n + 1 e guarda o resultado em n":
n = n + 1

# Podemos usar a função "print" para mostrar o valor de uma variável:
n = 10
print("==> o valor de n é", n)
n = n + 1
print("==> depois de n = n + 1:", n)


# ----------------------------------------------------------------------
# 2. Saída e entrada de dados

# A função input() lê uma linha do teclado e devolve uma str.
nome = input("Qual é o seu nome? ")
print("Olá,", nome, "!")

print()  # Um print vazio apenas imprime uma linha em branco.

# input() devolve sempre uma str (mesmo quando se escreve um número no teclado)
# É preciso converter antes de calcular.
altura = float(input("Altura da torre em metros: "))
print("Altura da torre é:", altura, "m")

print()  # Um print vazio apenas imprime uma linha em branco.

# Para confirmar um tipo de uma variável, usa-se a função type():
print("tipo da variável nome:", type(nome))
print("tipo da variável altura:", type(altura))


# ----------------------------------------------------------------------
# 3. Aritmética
a, b = 7, 2  # atribuição múltipla numa só linha

print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b, " <- divisão real: dá float mesmo com inteiros")
print("a // b =", a // b, "   <- divisão inteira (trunca)")
print("a % b  =", a % b, "   <- resto da divisão")
print("a ** b =", a**b, "  <- potência (não é ^)")

# Modificadores: atalhos para "atualizar" uma variável.
c = 10
c += 5  # equivale a c = c + 5
c *= 2  # equivale a c = c * 2
print("c =", c)

# ----------------------------------------------------------------------
# 4. O package math
import math

print("math.sqrt(2)      =", math.sqrt(2))
print("math.sin(math.pi) =", math.sin(math.pi), "  <- não é exatamente 0")
print("math.log(math.e)  =", math.log(math.e), "   <- log é o logaritmo natural")
print("math.log10(1000)  =", math.log10(1000))

# Alternativa: importar nomes individuais para o espaço de nomes atual.
from math import sqrt, pi

print("sqrt(2) =", sqrt(2), "  pi =", pi)
# Atenção: as funções de math trabalham com um número de cada vez.

# ----------------------------------------------------------------------
# 5. Funções pré-definidas
valores = [3.7, -1.2, 8.4, 0.5]
print("abs(-1.2)      =", abs(-1.2))
print("max(valores)   =", max(valores))
print("min(valores)   =", min(valores))
print("sum(valores)   =", sum(valores))
print("len(valores)   =", len(valores))
print("round(3.7)     =", round(3.7))
print("int(3.7)       =", int(3.7), "   <- trunca, não arredonda")
print("float('2.5')   =", float("2.5"))
print("str(42) + '!'  =", str(42) + "!")


# ----------------------------------------------------------------------
# 6. Decisões: if / elif / else
# O bloco pertencente ao if é definido pela indentação (4 espaços).
velocidade = 12.0  # m/s

if velocidade > 20.0:
    regime = "rápido"
elif velocidade > 5.0:
    regime = "moderado"
else:
    regime = "lento"

print("velocidade =", velocidade, "->", regime)

print()

# Comparações:  ==  !=  <  <=  >  >=
# Combinam-se com and, or, not
print("0 < velocidade < 15 ?", 0 < velocidade < 15)
print("1 é igual a 1?", 1 == 1)
print("1 é diferente de 10?", 1 != 10)
print("1 é igual a 1 e 1 é diferente de 10?", 1 == 1 and 1 != 10)

print()

# Nunca testar igualdade exata entre floats:
print("0.1 + 0.2 == 0.3 ?", 0.1 + 0.2 == 0.3)
print("abs(0.1 + 0.2 - 0.3) > 1e-18 ?", abs(0.1 + 0.2 - 0.3) > 1e-18)


# ----------------------------------------------------------------------
# 7. Ciclos while
# Menor potência de 2 que excede 1000.
k, potencia = 0, 1
while potencia <= 1000:
    k += 1
    potencia *= 2
print("2 **", k, "=", potencia)


# ----------------------------------------------------------------------
# 8. Ciclos for
for i in range(5):  # 0, 1, 2, 3, 4 — o fim é exclusivo
    print("  i =", i, " i² =", i**2)

print()

print("range(2, 11, 3) ->", list(range(2, 11, 3)))

print()

alturas = [10.0, 25.5, 100.0]  # lista: ordenada, mutável, heterogénea
for h in alturas:  # percorre diretamente os elementos
    print("  altura:", h, "m")

print()

for indice, h in enumerate(alturas):  # quando o índice também é preciso
    print("  alturas[%d] = %.1f" % (indice, h))

# ----------------------------------------------------------------------
# 9. Listas
alturas = [10.0, 25.5, 100.0]  # lista: ordenada, mutável, heterogénea
alturas.append(300.0)  # acrescenta ao fim

print("alturas      =", alturas)
print("alturas[0]   =", alturas[0], "  <- os índices começam em 0")
print("alturas[-1]  =", alturas[-1], " <- índice negativo conta do fim")
print("alturas[1:3] =", alturas[1:3], "  <- fatia: inclui 1, exclui 3")
print("len / sum    =", len(alturas), sum(alturas))

# Uma lista pode ser construída a partir de outra (list comprehension):
quadrados = [h**2 for h in alturas]
print("quadrados    =", quadrados)


# ----------------------------------------------------------------------
# 10. Arrays de numpy

# Precisamos de importar uma biblioteca externa para trabalhar com arrays,
# que são mais eficientes do que listas.
import numpy as np  # a biblioteca chama-se "numpy" e é importada com o nome "np"

t = np.linspace(0.0, 5.0, 6)  # 6 valores igualmente espaçados de 0 a 5
print("t          =", t)
print("np.zeros(4)=", np.zeros(4))
print("np.arange(0, 1, 0.25) =", np.arange(0.0, 1.0, 0.25))

print()

# Diferença essencial entre lista e array:
print("[1, 2] * 2 =", [1, 2] * 2, "   <- a lista repete-se")
print("np.array([1, 2]) * 2 =", np.array([1, 2]) * 2, "  <- o array multiplica")

print()

# As operações aplicam-se elemento a elemento, sem ciclo explícito.
g = 9.81
y = 0.5 * g * t**2
print("y = ½gt²   =", y)
print("np.sqrt(t) =", np.sqrt(t))

print()

u = np.array([1.0, 0.0, 0.0])
v = np.array([0.0, 2.0, 0.0])
print("produto interno u·v =", np.dot(u, v))
print("norma de v          =", np.sqrt(np.dot(v, v)))


# ----------------------------------------------------------------------
# 11. Funções definidas pelo utilizador


def tempo_de_queda(altura, g=9.81):
    """Tempo de queda livre a partir do repouso, de uma dada altura.

    Parâmetros
    ----------
    altura : float
        Altura inicial, em metros.
    g : float
        Aceleração gravítica, em m/s². Por omissão, 9.81.

    Devolve
    -------
    float
        Tempo de queda, em segundos.
    """
    tempo_de_queda = math.sqrt(2.0 * altura / g)
    return tempo_de_queda


# chamar uma função
print("tempo_de_queda(100)            =", tempo_de_queda(100.0))
# chamar a função com um argumento diferente para o valor de g
print("tempo_de_queda(100, g=1.62)    =", tempo_de_queda(100.0, g=1.62))

print()
