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

# %%
