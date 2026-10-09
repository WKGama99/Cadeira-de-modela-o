#%%

import matplotlib.pyplot as plt
import numpy as np

# a)
theta = np.linspace(0, 2 * np.pi, 100)

x = 2 * np.cos(theta) + np.cos(2 * theta)
y = 2 * np.sin(theta) - np.sin(2 * theta)

plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# b)
theta = np.linspace(0, 10 * np.pi, 1000)
r = theta**2

x = r * np.cos(theta)
y = r * np.sin(theta)
plt.plot(x, y)
plt.title("Galilean Spiral")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# c)
theta = np.linspace(0, 24 * np.pi, 10000)
r = np.exp(np.cos(theta)) - 2 * np.cos(4 * theta) + np.sin(theta / 12) ** 5

x = r * np.cos(theta)
y = r * np.sin(theta)
plt.plot(x, y)
plt.title("Função de Fey")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
# %%
import pint

ureg = pint.UnitRegistry()

velocidade = 120 * (ureg.kilometer / ureg.hour)
tempo = 15 * ureg.minute

print("--- Dados Iniciais---")
print (f"Velocidade: (velocidade)")
print(f"Tempo: ")