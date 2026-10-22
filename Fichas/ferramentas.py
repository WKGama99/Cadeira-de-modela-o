"""
MCSF — Aula P05: ferramentas fornecidas (NÃO é preciso alterar este ficheiro).

Contém:
  - os parâmetros físicos do problema;
  - a solução exata da queda vertical (para validar);
  - funções para desenhar gráficos e animar a trajetória.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------------------------------------------------------
# Parâmetros físicos (tabela da aula TP)
# ------------------------------------------------------------------
M = 80.0  # massa do paraquedista + equipamento [kg]
G = 9.81  # aceleração gravítica [m/s²]
RHO = 1.225  # densidade do ar (atmosfera padrão, nível do mar) [kg/m³]

CD_LIVRE, A_LIVRE = 1.0, 0.70  # corpo na horizontal: 2 m × 0,35 m
CD_PARAQUEDAS = 0.8  # calote circular plana
D_PARAQUEDAS = 10.7  # diâmetro da calote [m]
A_PARAQUEDAS = np.pi * D_PARAQUEDAS**2 / 4  # ≈ 89,9 m²

K_LIVRE = 0.5 * RHO * CD_LIVRE * A_LIVRE  # ≈ 0,43 kg/m
K_PARAQUEDAS = 0.5 * RHO * CD_PARAQUEDAS * A_PARAQUEDAS  # ≈ 44 kg/m


# ------------------------------------------------------------------
# Referência analítica
# ------------------------------------------------------------------
def v_exata(t, m=M, g=G, k=K_LIVRE):
    """Velocidade de queda (positiva para baixo) de um corpo largado do repouso,
    com arrasto k v². Solução exata: v(t) = v_t tanh(g t / v_t)."""
    vt = np.sqrt(m * g / k)
    return vt * np.tanh(g * np.asarray(t) / vt)


# ------------------------------------------------------------------
# Gráficos
# ------------------------------------------------------------------
def grafico(t, *series, legendas=None, xlabel="t (s)", ylabel="", titulo=""):
    """Desenha uma ou mais séries em função de t.
    Exemplo: grafico(t, v, v_exata(t), legendas=["Euler", "exata"], ylabel="v (m/s)")"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, s in enumerate(series):
        rot = legendas[i] if legendas else None
        estilo = "o-" if (i == 0 and len(t) <= 40) else "-"
        ax.plot(t, s, estilo, label=rot, ms=4)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.grid(alpha=0.3)
    if legendas:
        ax.legend()
    plt.tight_layout()
    plt.show()


def trajetoria(*pares, legendas=None, titulo=""):
    """Desenha trajetórias y(x). Exemplo: trajetoria((x1, y1), (x2, y2), legendas=["a", "b"])"""
    fig, ax = plt.subplots(figsize=(6, 6))
    for i, (x, y) in enumerate(pares):
        ax.plot(x, y, label=legendas[i] if legendas else None)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("altitude (m)")
    ax.set_title(titulo)
    ax.grid(alpha=0.3)
    if legendas:
        ax.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------
# Animação
# ------------------------------------------------------------------
def animar(t, x, y, vx, vy, ritmo=10.0, fps=25, aberto=None):
    """Anima a trajetória a partir dos vossos arrays.

    ritmo  : segundos simulados por segundo de animação (velocidade de reprodução)
    fps    : fotogramas por segundo (suavidade)
    aberto : array booleano opcional (True quando o paraquedas está aberto)

    Nota: o passo da simulação (Δt), o ritmo e os fps são três coisas independentes.
    """
    t, x, y, vx, vy = map(np.asarray, (t, x, y, vx, vy))
    tempos = np.arange(0, t[-1], ritmo / fps)
    idx = np.minimum(np.searchsorted(t, tempos), len(t) - 1)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(min(x.min(), 0) - 50, x.max() + 100)
    ax.set_ylim(0, y.max() * 1.05)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("altitude (m)")
    ax.grid(alpha=0.3)
    (rasto,) = ax.plot([], [], "-", color="tab:blue", lw=2)
    (ponto,) = ax.plot([], [], "o", color="tab:blue", ms=9)
    seta = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color="tab:green", lw=2),
    )
    texto = ax.text(
        0.02,
        0.02,
        "",
        transform=ax.transAxes,
        family="monospace",
        fontsize=10,
        bbox=dict(fc="white", ec="0.8"),
    )

    def atualizar(n):
        i = idx[n]
        rasto.set_data(x[: i + 1], y[: i + 1])
        ponto.set_data([x[i]], [y[i]])
        if aberto is not None:
            ponto.set_color("tab:orange" if aberto[i] else "tab:blue")
        esc = 5.0
        seta.set_position((x[i], y[i]))
        seta.xy = (x[i] + esc * vx[i], y[i] + esc * vy[i])
        v = np.hypot(vx[i], vy[i])
        texto.set_text(
            f"t = {t[i]:6.1f} s\naltitude = {y[i]:6.0f} m\n|v| = {v:5.1f} m/s"
        )
        return rasto, ponto, seta, texto

    anim = FuncAnimation(
        fig, atualizar, frames=len(idx), interval=1000 / fps, blit=False, repeat=False
    )
    plt.show()
    return anim
