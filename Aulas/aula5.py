#%%

m = 80
g = 9.81
p = 1.225
c = 1.0 
a = 0.7


k = 1/2 * p * c * a 
print(k)
#%%
m = 80
g = 9.81
p = 1.225
c = 0.8
a = 89

k = 1/2 * p * c * a

print(k)
# %%
import numpy as np

m = 80
g = 9.81
k = 0.429

v = np.sqrt (m * g / k)


print(k)
# %%
# feito pelo professor

g = 9.81
m = 80

rho = 1.225

C_d_ql = 1
C_d_p = 0.8

A_ql = 0.7
A_p = 89

k_ql = (1/2) * rho * C_d_ql * A_ql
k_p = (1/2) * rho * C_d_p * A_p

print(f"k_q = {k_ql:.3f} ; k_p = {k_p:.3f};")
# %%
#exercicio 2 feito pelo professro

v_ql_ms = np.sqrt((m * g) / k_ql)
v_ql_kmh = v_ql_ms * 3.6

v_p_ms = np.sqrt((m * g) / k_p)
v_p_kmh = v_p_ms * 3.6

print(f"Queda livre: v_t = {v_ql_ms:.2f} m/s | v_t = {v_ql_kmh:.2f} km/h")
print(f"Paraquedas aberto: v_t = {v_p_ms:.2f} m/s | v_t = {v_p_kmh:.2f} km/h")
# %%
#exercicio 3 feito pelo professor

razao = v_ql_ms / v_p_ms

print(  f"A velocidade terminal é dividida por aproximadamente {razao:.2f} vezes.")