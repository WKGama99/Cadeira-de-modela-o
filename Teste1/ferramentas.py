"""
ferramentas.py — E1: paragem de emergência de um AGV
Parâmetros da ficha técnica, leitura de dados, solução exata e gráficos.
NÃO ALTERAR ESTE FICHEIRO.
"""
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Ficha técnica do AGV (valores nominais) ----------------
G = 9.81        # aceleração da gravidade (m/s²)
M = 400.0       # massa do AGV com a carga de referência (kg)
MU = 0.03       # coeficiente de atrito (rolamento + travão mecânico)
B = 200.0       # coeficiente de travagem do motor (N·s/m)
V0 = 2.0        # velocidade de cruzeiro (m/s)
T_TRAVAGEM = 1.0  # instante do comando de paragem no registo do encoder (s)


def carregar_dados(nome="agv_travagem.csv"):
    """Lê o registo do encoder. Devolve os arrays t (s) e x (m)."""
    dados = np.loadtxt(nome, delimiter=",", skiprows=1)
    return dados[:, 0], dados[:, 1]


def solucao_exata(t, v0, mu_g, b_m):
    """
    Solução exata de a = -mu_g - b_m * v, com v(0) = v0 e x(0) = 0.
    O tempo t conta a partir do comando de paragem. Depois de parar, x e v ficam constantes.
    Devolve x(t), v(t) e a duração da travagem t_p.
    """
    t = np.asarray(t, dtype=float)
    c = mu_g / b_m
    t_p = np.log(1 + v0 / c) / b_m
    tau = np.clip(t, 0.0, t_p)
    x = (v0 + c) / b_m * (1 - np.exp(-b_m * tau)) - c * tau
    v = (v0 + c) * np.exp(-b_m * tau) - c
    return x, v, t_p


# ------------------------------- Gráficos -------------------------------
def grafico_x_v(t, x, v):
    """Posição e velocidade lado a lado."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(t, x, ".", ms=3)
    ax1.set(title="Posição (encoder)", xlabel="t (s)", ylabel="x (m)")
    ax2.plot(t, v, "-", lw=1)
    ax2.set(title="Velocidade (np.gradient)", xlabel="t (s)", ylabel="v (m/s)")
    for ax in (ax1, ax2):
        ax.axvline(T_TRAVAGEM, color="grey", ls=":", lw=1)
        ax.grid(alpha=0.3)
    fig.tight_layout()
    plt.show()


def grafico_aceleracoes(resultados):
    """resultados: lista de (k, tk, ak). Desenha a(t) para cada k."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for k, tk, ak in resultados:
        ax.plot(tk, ak, "o-" if k > 3 else "-", ms=3, lw=0.8, label=f"k = {k}")
    ax.axvline(T_TRAVAGEM, color="grey", ls=":", lw=1)
    ax.set(title="Aceleração estimada", xlabel="t (s)", ylabel="a (m/s²)", ylim=(-4, 3))
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    plt.show()


def grafico_a_v(vk, ak, mu_g=None, b_m=None):
    """a em função de v durante a travagem; se mu_g e b_m forem dados, desenha a reta do modelo."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(vk, ak, "o", label="dados")
    if mu_g is not None and b_m is not None:
        vv = np.linspace(0, V0, 20)
        ax.plot(vv, -mu_g - b_m * vv, "k--", label="modelo identificado")
    ax.set(title="a(v) durante a travagem", xlabel="v (m/s)", ylabel="a (m/s²)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    plt.show()


def grafico_euler(t_sim, x_sim, v_sim, t_dados=None, x_dados=None, mu_g=None, b_m=None):
    """Simulação de Euler, solução exata (se mu_g e b_m forem dados) e dados do encoder."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(t_sim, x_sim, "-", label="Euler")
    ax2.plot(t_sim, v_sim, "-", label="Euler")
    if mu_g is not None and b_m is not None:
        tt = np.linspace(0, t_sim[-1], 300)
        xe, ve, _ = solucao_exata(tt, V0, mu_g, b_m)
        ax1.plot(tt, xe, "k--", lw=1, label="exata")
        ax2.plot(tt, ve, "k--", lw=1, label="exata")
    if t_dados is not None:
        ax1.plot(t_dados, x_dados, ".", ms=3, label="encoder")
    ax1.set(title="Posição desde o comando de paragem", xlabel="t (s)", ylabel="x (m)")
    ax2.set(title="Velocidade", xlabel="t (s)", ylabel="v (m/s)")
    for ax in (ax1, ax2):
        ax.grid(alpha=0.3)
        ax.legend()
    fig.tight_layout()
    plt.show()
