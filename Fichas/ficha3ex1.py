#%%
import numpy as np 

t = np.array ([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
d = np.array ([0.000, 0.049, 0.196, 0.441, 0.784, 1.225])
dt = 0.1
v = np.diff(d) / dt

print (v)
#%%
a = np.diff(v) / dt

print("Acelarações:", np.round(a,2))
print("Tamanhos - t:", len(t), " v:", len(v), " a:", len(a))
# %% 
t_v = t[:-1] + (dt / 2)
v_exata = 9.8 * t_v
print("Velocidades exatas:", np.round(v_exata, 2))

acelaração_correta = np.isclose(a, 9.8)
print("Todas as acelerações são quase iguais a 9.8?", np.all(acelaração_correta))
# %%
