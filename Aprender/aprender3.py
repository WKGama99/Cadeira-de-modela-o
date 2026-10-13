#%%
import math as mp

h = float(input("Introduza a altura da torre:"))
g = 9.81

raiz = mp.sqrt ((2 * h) / g)

print (raiz)

# %%
import numpy as np
t = float(input("Introduza o valor de t:"))
g = 6.67 * 10 ** -11
m = 5.97 * 10 ** 24
r = 6371 * 1000



h = ((g * m * (t**2)) / (4 * np.pi **2)) ** (1/3) - r


print(h)
# %%
import numpy as np


G = 6.67e-11       
M = 5.97e24        
R = 6371 * 1000    


T = float(input("Introduza o período T (em segundos): "))


h = ((G * M * (T**2)) / (4 * np.pi**2))**(1/3) - R


print(f"A altitude necessária do satélite é: {h:.2f} metros")

#%%

import matplotlib.pyplot as plt
import numpy as np

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
temperatura = [20, 21, 22, 23, 24, 25, 26]

plt.plot(dias, temperatura, marker= "o", color= "blue", linestyle= "--", linewidth=2)
plt.title("Temperatura durante a semana")
plt.xlabel("Dias da semana")
plt.ylabel("Temperatura (ºC)")


plt.show()
# %%
