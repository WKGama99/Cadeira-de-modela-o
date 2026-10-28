"""
Ficha de revisão — Parte 2: arranque do rebocador medido por um tacómetro
Complete apenas os blocos marcados com # TODO. Corra com: python revisao.py
Cada parte usa resultados das anteriores: faça-as por ordem.
"""
import numpy as np
import matplotlib.pyplot as plt

MOSTRAR_GRAFICOS = True  # pode pôr False enquanto testa, para não abrir janelas

# ------------------- Ficha técnica e funções auxiliares (NÃO ALTERAR) -------------------
G, M, F, MU, B = 9.81, 600.0, 600.0, 0.02, 240.0   # SI
T_ARRANQUE = 3.0                                    # instante do arranque no registo (s)


def solucao_exata(t, a0, b_m):
    """x(t) e v(t) a partir do repouso, com a = a0 - b_m*v; t conta a partir do arranque."""
    t = np.clip(np.asarray(t, dtype=float), 0.0, None)
    v_lim = a0 / b_m
    return v_lim * (t - (1 - np.exp(-b_m * t)) / b_m), v_lim * (1 - np.exp(-b_m * t))


def grafico(series, titulo, ylabel, linha_v=None):
    """series: lista de (t, y, rótulo, estilo)."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for tt, yy, rotulo, estilo in series:
        ax.plot(tt, yy, estilo, ms=3, lw=1, label=rotulo)
    if linha_v is not None:
        ax.axvline(linha_v, color="grey", ls=":", lw=1)
    ax.set(title=titulo, xlabel="t (s)", ylabel=ylabel)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    plt.show()
# -----------------------------------------------------------------------------------------

dados = np.loadtxt("tacometro_arranque.csv", delimiter=",", skiprows=1)
t, v = dados[:, 0], dados[:, 1]

# =============================================================================
# PARTE A — Leitura dos dados e deteção do arranque
# =============================================================================
#TODO A(a): número de leituras, passo temporal e último instante do registo
N = len(t)
dt = t[1] - t[0]
t_final = t[-1]
print(f"[PARTE A] N = {N}, dt = {dt:.3f} s, último instante = {t_final:.1f} s")

# TODO A(b): média e desvio-padrão da velocidade medida com o rebocador parado (t < 2,9 s)
em_repouso = t < 2.9
v_media_repouso = np.mean(v[em_repouso])
sigma_v = np.std(v[em_repouso])

print(f"[PARTE A] em repouso: média = {v_media_repouso:.4f} m/s, desvio-padrão = {sigma_v:.4f} m/s")
print(f"[PARTE A] Há valores negativos em repouso? {np.any(v[t < 2.9] < 0)}")

# TODO A(c): índice da PRIMEIRA leitura com v > 0,1 m/s e instante correspondente
i_arr = np.argmax(v > 0.1)
print(
    f"[PARTE A] arranque detetado no índice {i_arr}, t = {t[i_arr]:.2f} s (arranque real: {T_ARRANQUE:.2f} s)")
if MOSTRAR_GRAFICOS:
    grafico([(t, v, "tacómetro", ".")], "Velocidade medida", "v (m/s)", T_ARRANQUE)

print()


# =============================================================================
# PARTE B — Aceleração a partir da velocidade (uma só derivada)
# =============================================================================
def derivada(t, v, k):
    """Usa uma leitura em cada k e deriva UMA vez com np.gradient. Devolve tk e ak."""
    # TODO B(a): subamostrar e derivar
    tk = t[::k]
    vk = v[::k]
    ak = np.gradient(vk, tk)
    return tk, ak


print("[PARTE B]  k   dt (s)   desvio-padrão de a em repouso (m/s²)   razão")
desvio_anterior = None
for k in [1, 2, 4, 8]:
    tk, ak = derivada(t, v, k)
    # TODO B(b): desvio-padrão de ak com o rebocador parado (tk < 2,8 s)
    desvio = np.std(ak[tk < 2.8])
    razao = "" if desvio_anterior is None else f"{desvio_anterior / desvio:.2f}"
    print(f"          {k:2d}   {k*dt:.2f}     {desvio:.3f}                                {razao}")
    desvio_anterior = desvio
if MOSTRAR_GRAFICOS:
    t1, a1 = derivada(t, v, 1)
    t8, a8 = derivada(t, v, 8)
    grafico([(t1, a1, "k = 1", "-"), (t8, a8, "k = 8", "o-")], "Aceleração estimada", "a (m/s²)", T_ARRANQUE)

print()

# =============================================================================
# PARTE C — Distância percorrida: integrar a velocidade com o método de Euler
# =============================================================================
# TODO C(a): ciclo de Euler sobre os DADOS: x[i+1] = x[i] + v[i]*dt, com x[0] = 0
x_dados = np.zeros(N)
for i in range(N - 1):
    x_dados[i + 1] = x_dados[i] + v[i] * dt 

# TODO C(b): a mesma distância total numa só linha, com uma fatia de v e np.sum
d_soma = np.sum(v[:-1]) * dt
a0_ficha = F / M - MU * G
x_ex, _ = solucao_exata(t_final - T_ARRANQUE, a0_ficha, B / M)
print(f"[PARTE C] distância (ciclo)  = {x_dados[-1]:.3f} m")
print(f"[PARTE C] distância (np.sum) = {d_soma:.3f} m")
print(f"[PARTE C] distância exata (ficha técnica) = {float(x_ex):.3f} m")

print()

# =============================================================================
# PARTE D — Constante de tempo, parâmetros e simulação
# =============================================================================
# TODO D(a): velocidade final (média para t > 14 s) e instante em que v atinge 63,2 % dela
v_fim = np.mean(v[t > 14])
i_63 = np.flatnonzero((t >= T_ARRANQUE) & (v >= 0.632 * v_fim))[0]
tau = t[i_63] - T_ARRANQUE
B_M = 1 / tau
A0 = v_fim * B_M
print(f"[PARTE D] v_fim = {v_fim:.3f} m/s; tau = {tau:.2f} s; b/m = {B_M:.3f} 1/s; a0 = {A0:.3f} m/s²")
print(f"[PARTE D] mu = {(F / M - A0) / G:.4f} (ficha {MU}); b = {B_M * M:.0f} N·s/m (ficha {B:.0f})")


def simular(a0, b_m, dt, t_max):
    """Euler a partir do repouso (t = 0 no arranque)."""
    t_s, v_s = [0.0], [0.0]
    for _ in range(int(round(t_max / dt))):
        # TODO D(b): passo de Euler, usando o último valor da lista v_s
        v_novo = v_s[-1] + (a0 - b_m * v_s[-1]) * dt
        t_s.append(t_s[-1] + dt)
        v_s.append(v_novo)
    return np.array(t_s), np.array(v_s)


t_s, v_s = simular(A0, B_M, dt, t_final - T_ARRANQUE)

# TODO D(c): diferença entre a simulação e as medições depois do arranque (raiz da média dos quadrados)
depois = t >= T_ARRANQUE
tempos_depois = t[depois] - T_ARRANQUE
v_simulada_nos_dados = np.interp(tempos_depois, t_s, v_s)
residuo = np.sqrt(np.mean((v[depois] - v_simulada_nos_dados) ** 2))
print(f"[PARTE D] {len(v_s)} pontos simulados, {np.sum(depois)} medições depois do arranque")
print(f"[PARTE D] resíduo = {residuo:.4f} m/s (compare com sigma_v da Parte A)")
if MOSTRAR_GRAFICOS:
    grafico([(t[depois] - T_ARRANQUE, v[depois], "tacómetro", "."), (t_s, v_s, "Euler", "-")],
            "Medição e simulação desde o arranque", "v (m/s)")
