#%%
#Exercício 1 alínea a)


import numpy as np

t = np.arange(0, 1.61, 0.1)
y = 1 + 8 * t - 4.9 * t**2
v_exata = 8 - 9.8 * t

v_num = np.gradient(y, t)

print(v_exata)
print("")
print(v_num)
#%%
#Exercício 1 alínea b)
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(t, y)
ax1.set_title("Position vs time")
ax1.set_xlabel("Time(s)")
ax1.set_ylabel("Position(m)")
ax2.plot(t, v_exata, label ="Exata")
ax2.plot(t, v_num, marker="o")
ax2.set_title("Velociadade Exata vs Velocidade Númerica")
ax2.set_xlabel("Tempo (t)")
ax2.set_ylabel("Velocidade(m/s)")
fig.show()


#%%
#Exercíco 1 alínea c)

erro = v_num - v_exata

print(np.round(erro, 4 ))

# %%
#Exercício 1 alínea d) 
print(f"Instante quando a bola atinge a altura máxima: {np.argmin (np.abs(v_exata))}")
print(f"Tempo em que v=o: {t[0]}s")

#%%
#Exercício 2 alínea a)
import numpy as np 
for N in [11, 21, 41, 81]:
    t = np.linspace(0, 2* np.pi, N)
    f = np.sin(t)
    df_exata = np.cos(t)
    df_num = np.gradient(f, t)

    erro_max = np.max(np.abs(df_exata - df_num))

    print(erro_max)

# %%
#Exercício 2 alínea b)
import matplotlib.pyplot as plt
t_11 = np.linspace(0, 2 * np.pi, 11)
df_num_11 = np.gradient(np.sin(t_11), t_11)

t_total = np.linspace(0, 2 * np.pi, 200)
df_exata_total = np.cos(t_total)

plt.plot(t_total , df_exata_total, "r-", label= "Exata : cos(t)")


plt.plot(t_11, df_num_11, 'bo', label='Estimativa np.gradient (N=11)')


plt.title('Derivada de sin(t) para N=11')
plt.xlabel('t (rad)')
plt.ylabel("f'(t)")
plt.legend()


plt.show()
# %%
#Exercício 2 alínea c)
NN = [11, 21, 41, 81]
erros = []

for N in NN: 
     t = np.linspace(0, 2* np.pi, N)
     f = np.sin(t)    
     df_exata = np.cos(t)
     df_num = np.gradient(f, t)
     erro_max = np.max(np.abs(df_exata - df_num)) 
     erros.append (erro_max)

print("Razão entre erros consecutivos ao duplicar N:")
for i in range(len(erros) - 1):
    razao = erros[i] / erros[i + 1]
    print(f"Erro(N={NN[i]}) / Erro(N={NN[i+1]}) = {razao:.2f}")
# %%
#Exercício 2 alínea d)

import numpy as np

for k in range(1, 16):
    h = 10.0 ** (-k)
    estimativa = (np.sin(1 + h) - np.sin(1 - h)) / (2 * h) # diferença central em t = 1
    print(
        f" h = 1e-{k:<2d} estimativa = {estimativa:.15f} "
        f"erro = {abs(estimativa - np.cos(1)):.1e}"
    )

#h = 1e-5  estimativa = 0.540302305856999 erro = 1.1e-11
# %%
