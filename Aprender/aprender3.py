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

import matplotlib.pyplot as plt
import numpy as np

velocidade = [110, 145, 180, 195, 199, 100, 90, 77, 44, 20, 4, 0]
distancia = [100, 95, 85, 80, 74, 72, 60, 57, 40, 32, 15, 0]


plt.plot(velocidade, distancia, marker= "o", color= "blue", linestyle="-", linewidth=3)
plt.title("Velocidade percorrida em x distância")
plt.xlabel("Velocidade (m)")
plt.ylabel("Distância percorrida")

plt.show()
# %%
import matplotlib.pyplot as plt
import numpy as np


distancia_m = [0, 100, 200, 300, 400]
vel_eletrico = [0, 120, 180, 210, 230]
vel_combustao = [0, 90, 150, 200, 240]

plt.plot(distancia_m, vel_eletrico, marker= "o", color= "red", linestyle="--", linewidth=2)
plt.plot(distancia_m, vel_combustao, marker= "o", color= "blue", linestyle= "-", linewidth= 2)

plt.title ("Corrida: Veículo combustão vs veículo elétrico")
plt.xlabel("Distância (metros)")
plt.ylabel("Velocidade (m/s)")

plt.show()
# %%
import matplotlib.pyplot as plt

# Os nossos dados
tempo_seg = [0, 2, 4, 6]
velocidade = [0, 100, 200, 300]

corridas = ['Mónaco', 'Monza', 'Spa']
pontos = [15, 25, 18]

# 1. Preparar uma janela mais larga (10 de largura, 4 de altura)
plt.figure(figsize=(10, 4))

# 2. Ativar o espaço da ESQUERDA e desenhar lá
plt.subplot(1, 2, 1)
plt.plot(tempo_seg, velocidade, color='blue', marker='o')
plt.title("Aceleração no Teste")
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (km/h)")

# 3. Ativar o espaço da DIREITA e desenhar lá
plt.subplot(1, 2, 2)
plt.bar(corridas, pontos, color='green')
plt.title("Pontos no Campeonato")
plt.xlabel("Pista")
plt.ylabel("Pontos")

# 4. Ajustar automaticamente os espaços para ficar perfeito
plt.tight_layout()

# 5. Mostrar o painel final
plt.show()

#%%

import matplotlib.pyplot as plt
# Dados das etapas
etapas = ['Partida', 'Subida', 'Topo', 'Descida', 'Chegada']

# Dados do Gráfico 1 (Altitude em metros)
altitude = [100, 850, 1200, 300, 50]

# Dados do Gráfico 2 (Combustível gasto em litros por etapa)
consumo = [2, 12, 4, 1, 3]

plt.figure(figsize= (10,5))

# O primeiro número (1): Indica o número de linhas da nossa grelha imaginária.
# O segundo número (2): Indica o número de colunas da grelha.
# O terceiro número (1): Indica a posição onde o gráfico atual vai ser desenhado.

plt.subplot(2, 1, 2)
plt.plot(etapas, altitude, color= "red", marker="o")
plt.title("Altitude ao longo das etapas")
plt.xlabel("Etapas")
plt.ylabel("Altitude")

plt.subplot(2, 1, 1)
plt.bar(etapas, consumo, color= "green")
plt.title("Consumo ao longo das etapas")
plt.xlabel("Etapas")
plt.ylabel("Consumo")

plt.tight_layout()

plt.show()
# %%
