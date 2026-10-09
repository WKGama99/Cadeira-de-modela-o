valor = float(input("Escreve num número para calcular o dobro:"))

dobro = valor * 2

print(f"O dobro de {valor} é {dobro}")

#%%

altura = float(input("Introduza a sua altura para acrescentar 10 cm:"))

aumento = altura + 0.10

print (f"O aumento de {altura} é {aumento}")
# %%
idade  = int(input("Qual a sua idade:"))


if idade >= 18:
    print("Pode entrar na tropa")

else:  
    print("Não pode entrar na tropa")
# %%
nota = float(input("Qual é a tua média do secundário?:"))


if nota >= 16.8:
    print("Pode entrar em engenharia informática")
else: 
    print("Não pode entrar em engenharia informática")
# %%
 
n = int(input("Introduz um número de 1 a 20:"))

if n >= 5:
    print("Pode começar a estudar")
else:
    print("Não pode começar a estudar")
# %%
print("Olá! Eu estou a aprender python.")
# %%
nome = ("Gustavo")

print("Olá", nome)
# %%
idade = 18

print("Tenho", idade, "anos" )
# %%
numero1 = 10
numero2 = 77

print (numero1 + numero2)
# %%
nome = (input("Qual o teu nome:"))

print ("Olá", nome)
# %%
idade = (input("Que idade tens"))

print ("Tens", idade)
# %%
n = int(input("Escreve um número:"))

dobro = n * 2

print (f"O valor do {n} é o {dobro}:")
# %%
comprimento = float(input("Qual é o comprimento?"))
largura = float(input("Qual é a largura?"))

area = comprimento + largura

print("A área é:", area )
# %%(
idade = int(input("Introduza a sua idade:"))

if idade >=18:
    print("É maior de idade")
else:
    print("Não é maior de idade")
# %%

n = float(input("Introduza um número:"))

if n >= 0: 
    print ("Número é positivo")
else: 
    print ("Número é negativo")
# %%

nota = float(input("Qual a tua nota no último jogo?:"))

if nota <= 4:
    print("Precisas de melhorar")
elif nota <= 6:
    print("Ainda podes melhorar mais")
elif nota <= 8:
    print("Já está melhor")
else: 
    print("Estás excelente")
    
# %%

a = int(input("Introduza um número inteiro:"))
b = int(input("Introduza o segundo número inteiro:"))

valor = a + b 

print (f"O soma de {a} e {b} é {valor} : ")


# %%
a = float(input("Introduza um número:"))
b = float(input("Introduza o segundo número:"))
c = float(input("Introduza o terceiro número:"))

valor = a * b + c

print (f"A multiplicação de {a} e {b} mais a soma de {c} é {valor} : ")
# %%
b = float(input("Introduza um número:"))
c = float(input("Introduza um segundo número para elevar o primeiro:"))

valor = b ** c
print(f"A elevação de {b} e {c} é {valor}")
# %%
import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-5, 5, 100)
y = x**2 - 4 * x + 3 

plt.figure(figsize=(8, 5))
plt.plot(x, y, color= "blue", linewidth = 2, label = "y = x**2 - 4x +3" )
plt.title("Gráfico da Função Quadrática")
plt.xlabel("Eixo X")
plt.ylabel("Eixo Y")


plt.axhline(0, color = "black", linewidth = 0.8, linestyle="--")
plt.axvline(0, color="black", linewidth= 0.8, linestyle="--")
plt.grid(True, linestyle=":", alpha=0.7)
plt.legend()

plt.show
# %%
nome = input("Introduza um nome")


print("Bem vindo", nome)
# %%
idade = input("Que idade tens?:")

print("Eu tenho", idade, "anos")
# %%
universidade = input("Em que universidade andas?:")


print("Ando na", universidade)
# %%
print("Olá, tudo bem?.")
# %%
