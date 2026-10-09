
import numpy as np
import matplotlib as plt 
dados = np.loadtxt("queda_livre_30fps.csv", delimiter=",", skiprows=1)

t = dados[:, 0]
d = dados[:, 1]

numero_fotogramas = len(t)
dt = np.mean(np.diff(t))

print("Número de fotogramaas:", numero_fotogramas)

dt = t[1] - t[0]
print("Passo temporal (dt):", np.round(dt, 4), "s")




