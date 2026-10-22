#%%
m = 80
k = 0.43
g = 9.81

v0 = 0
dt = 1

# a = g - (k/m) v**2

# primeira iteração  
a0 = g - (k/m) * v0**2
v1 = v0 + a0 * dt

print(f"Velocidade na primeira iter: {v1}")
print(f"Acelaração na primeira inter: {a0}")
#%%

#segunda iteração
a1 = g - (k/m) * v1**2
v2 = v1 + a1* dt

print(f"Velocidade na segunda iter: {v2}")
print(f"Acelaração na segunda inter: {a1}")
# %%

a2 = g - (k/m) * v2**2
v3 = v2 + a2 * dt
print(f"Velocidade na terceira iter: {v3}")
print(f"Acelaração na terceira inter: {a2}")
# %%
a3 = g - (k/m) * v3**2
v4 = v3 + a3 * dt
print(f"Velocidade na quarta inter: {v4}")
print(f"Acelaração na quarta inter: {a3}")
# %%

a3 = g - (k/m) * v3**2
v4 = v3 + a3 * dt

a4 = g - (k/m) * v3**2
v5 = v4 + a4 * dt


#%%
v = [v0, v1, v2, v3, v4, v5]
x = [0, dt, 2*dt, 3*dt, 4*dt, 5*dt]

#%%
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()

plt.plot(x, v, marker="o", label="Velocidade")

y = np.linspace(0, 5, 100)
xx = y
plt.plot(xx, y, linestyle="--", c="k", label="Referencia")

plt.legend()
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (m/s) ")
plt.title("Velocidade em função do tempo")
plt.show()

# %%
