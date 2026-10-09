import numpy as np

dados = np.loadtxt("queda_livre_30fps.csv", delimiter= ",", skiprows= 1 )
t = dados[:, 0]
d = dados[:, 1]
dt = t[1] - t[0]

v = np.diff(d) / dt
a = np.diff(v) / dt
t_v = t[:-1] + (dt / 2)
t_a = t_v[:-1] + (dt / 2)

print("Velocidades (v):", np.round(v, 2))
print("Instantes (t_v):", np.round(t_v, 3))
print("Acelerações (a):", np.round(a, 2))
print("Instantes (t_a):", np.round(t_a, 3))
