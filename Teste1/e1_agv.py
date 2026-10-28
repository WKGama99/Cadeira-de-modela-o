"""
E1 — Paragem de emergência de um AGV
Complete apenas os blocos marcados com # TODO. Corra com: python e1_agv.py
Cada parte usa resultados das anteriores: faça-as por ordem.
"""

import numpy as np
from ferramentas import (
    G,
    M,
    MU,
    B,
    V0,
    T_TRAVAGEM,
    carregar_dados,
    solucao_exata,
    grafico_x_v,
    grafico_aceleracoes,
    grafico_a_v,
    grafico_euler,
)

MOSTRAR_GRAFICOS = True  # pode pôr False enquanto testa, para não abrir janelas

# =============================================================================
# PARTE A — Velocidade a partir do encoder
# =============================================================================
t, x = carregar_dados("agv_travagem.csv")

# TODO A(a): número de leituras e passo temporal
N = len(t)
dt = t[1] - t[0]
print(f"[PARTE A] N = {N}, dt = {dt:.3f} s")

# TODO A(b): velocidade com np.gradient
v = np.gradient (x, t)
if MOSTRAR_GRAFICOS:
    grafico_x_v(t, x, v)

# TODO A(c): velocidade média em cruzeiro (t < 0,9 s)
v_cruzeiro = np.mean(v[t < 0.9])
i_trav = np.argmin(np.abs(t - T_TRAVAGEM))
d_medida = np.mean(x[t > 5]) - x[i_trav]
print(
    f"[PARTE A] v em cruzeiro = {v_cruzeiro:.3f} m/s; distância de paragem medida = {d_medida:.3f} m"
)
print(f"[PARTE A] Há algum v exatamente igual a 0? {np.any(v == 0)}")

print("\n" * 4)


# =============================================================================
# PARTE B — Aceleração e ruído
# =============================================================================
def derivadas(t, x, k):
    """Usa uma leitura em cada k. Devolve tk, vk (velocidade) e ak (aceleração), todos com o mesmo tamanho."""
    # TODO B(a): subamostrar e derivar duas vezes com np.gradient
    #           (uma vez para determinar as velocidades, vk, e outra para as acelerações, ak)
    tk = t[::k]
    xk = x[::k]
    vk = np.gradient(xk, tk)
    ak = np.gradient(vk, tk)
    return tk, vk, ak


resultados = []
print("[PARTE B]  k   dt (s)   desvio-padrão de a com o AGV parado (m/s²)")
for k in [1, 2, 3, 5]:
    tk, vk, ak = derivadas(t, x, k)
    # TODO B(b): desvio-padrão de ak quando o AGV já está parado (tk > 4,5 s)
    desvio = np.std(ak[tk > 4.5])
    print(f"    {k:2d}   {k*dt:.2f}     {desvio:.3f}")
    resultados.append((k, tk, ak))
if MOSTRAR_GRAFICOS:
    t15, _, a15 = derivadas(t, x, 15)
    grafico_aceleracoes([resultados[3], (15, t15, a15)])

print("\n" * 4)

# =============================================================================
# PARTE C — Identificação dos parâmetros do modelo a = -mu*g - (b/m)*v
# =============================================================================
T1, T2 = 1.5, 3.0  # 0,5 s e 2,0 s depois do comando de paragem


def identificar(tk, vk, ak):
    """Estima mu*g e b/m a partir de dois pontos da reta a(v), nos instantes mais próximos de T1 e T2."""
    i1 = np.argmin(np.abs(tk - T1))
    i2 = np.argmin(np.abs(tk - T2))
    # TODO C(a): declive e ordenada na origem da reta que passa pelos dois pontos
    declive = (ak[i2] - ak[i1]) / (vk[i2] - vk[i1])
    b_m = -declive
    mu_g = -(ak[i1] - declive * vk[i1])
    return mu_g, b_m


print("[PARTE C]  k   dt (s)   mu*g (m/s²)   b/m (1/s)")
for k in [1, 2, 3, 5, 8, 10, 15, 20, 25]:
    mu_g_k, b_m_k = identificar(*derivadas(t, x, k))
    print(f"          {k:2d}   {k*dt:.2f}     {mu_g_k:7.3f}      {b_m_k:7.3f}")

# TODO C(b): escolha o valor de k que considera mais fiável (justifique no relatório)
K = 15
tk, vk, ak = derivadas(t, x, K)
MU_G, B_M = identificar(tk, vk, ak)
print(
    f"[PARTE C] k = {K}: mu = {MU_G/G:.4f} (ficha técnica {MU}); b = {B_M*M:.1f} N·s/m (ficha técnica {B:.0f})"
)
if MOSTRAR_GRAFICOS:
    durante = (tk > T_TRAVAGEM + 0.3) & (tk < 3.7)
    grafico_a_v(vk[durante], ak[durante], MU_G, B_M)

print("\n" * 4)


# =============================================================================
# PARTE D — Simulação com o método de Euler
# =============================================================================
def aceleracao(v, mu_g, b_m):
    # TODO D(a): aceleração do modelo
    return -mu_g - b_m * v


def simular(v0, mu_g, b_m, dt, parar=True, t_max=10.0):
    """Euler a partir do comando de paragem (t = 0, x = 0, v = v0)."""
    t_s, x_s, v_s = [0.0], [0.0], [v0]
    for _ in range(int(round(t_max / dt))):
        a = aceleracao(v_s[-1], mu_g, b_m)
        # TODO D(b): passo de Euler para v e x
        #       dica: veja como a aceleracao é calculada em cima - repare que usa o índice -1
        #             para o último valor de v e x
        v_novo = v_s[-1] + a * dt
        x_novo = x_s[-1] + v_s[-1] * dt
        # TODO D(c): condição de paragem — se v_novo deixar de ser positiva (<=0), o AGV parou
        if parar and v_novo <= 0:
            t_s.append(t_s[-1] + dt)
            x_s.append(x_novo)
            v_s.append(0.0)
            break
        t_s.append(t_s[-1] + dt)
        x_s.append(x_novo)
        v_s.append(v_novo)
    return np.array(t_s), np.array(x_s), np.array(v_s)


t_s, x_s, v_s = simular(V0, MU_G, B_M, 0.01)
_, _, t_p = solucao_exata(0, V0, MU_G, B_M)
x_p, _, _ = solucao_exata(t_p, V0, MU_G, B_M)
print(
    f"[PARTE D] Euler (dt = 0,01 s): para ao fim de {t_s[-1]:.2f} s, a {x_s[-1]:.3f} m"
)
print(
    f"[PARTE D] Exata:                para ao fim de {t_p:.2f} s, a {float(x_p):.3f} m"
)
print(f"[PARTE D] Encoder:              distância de paragem {d_medida:.3f} m")
if MOSTRAR_GRAFICOS:
    depois = t >= T_TRAVAGEM
    grafico_euler(
        t_s, x_s, v_s, t[depois] - T_TRAVAGEM, x[depois] - x[i_trav], MU_G, B_M
    )

print("\n" * 4)
