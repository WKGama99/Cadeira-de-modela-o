"""
MCSF — Simulador interativo do salto de paraquedas (2D, método de Euler)
=========================================================================

Corre com:  python simulador_salto.py
Só precisa de numpy e matplotlib (os controlos são os "widgets" do próprio matplotlib).

Mexa nos controlos do lado direito e a simulação é refeita de imediato.
O botão "Fixar referência" guarda a simulação atual a cinzento, para comparar com a seguinte.

O ficheiro está organizado em quatro partes, pela ordem em que as usamos nas aulas:

  1. PARÂMETROS      — os valores do problema (os mesmos das aulas TP e P)
  2. MODELO FÍSICO   — as forças: peso + arrasto, e como o arrasto muda quando o paraquedas abre
  3. MÉTODO NUMÉRICO — o passo de Euler, aplicado a x, y, v_x e v_y
  4. INTERFACE       — gráficos e controlos (não é preciso ler para perceber a física)

Convenção: y é a ALTITUDE e aponta PARA CIMA (como nas Etapas 2 a 4).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# =============================================================================
# 1. PARÂMETROS
# =============================================================================
G = 9.81  # aceleração da gravidade [m/s²]
RHO = 1.225  # densidade do ar, atmosfera padrão ao nível do mar [kg/m³]

CD_CORPO, A_CORPO = 1.0, 0.70  # corpo na horizontal (barriga para baixo): 2 m × 0,35 m
CD_PARAQUEDAS = 0.8  # calote circular plana

# Valores iniciais dos controlos (podem ser alterados na interface)
INICIAIS = dict(
    massa=80.0,  # massa do paraquedista + equipamento [kg]
    y0=3000.0,  # altitude de saída do avião [m]
    vx0=50.0,  # velocidade horizontal do avião [m/s]
    h_abertura=900.0,  # altitude a que o paraquedas é acionado [m]
    t_enchimento=0.0,  # tempo que a calote demora a encher [s] (0 = abertura instantânea)
    diametro=10.7,  # diâmetro da calote [m]
    dt=0.01,  # passo de tempo do método de Euler [s]
)
PASSOS_DT = [0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]  # valores possíveis de Δt
T_MAX = 900.0  # tempo máximo simulado [s]


def constante_arrasto(cd, area):
    """k = ½ rho C_d A   [kg/m].  Arrasto quadrático: |F_a| = k v²."""
    return 0.5 * RHO * cd * area


# =============================================================================
# 2. MODELO FÍSICO
# =============================================================================
# Forças (y para cima):
#     peso      P   = (0, -m g)
#     arrasto   F_a = -k |v| v       → oposto à velocidade, com módulo k v²
#
# 2.ª lei de Newton, por componentes:
#     a_x = -(k/m) |v| v_x
#     a_y = -g - (k/m) |v| v_y
#
# O que muda ao longo do salto é só a constante de arrasto k:
#
#   k
#   ^
#   |                      ______________________  k_paraquedas  (≈ 44 kg/m)
#   |                     /
#   |                    /   ← enchimento: a calote demora t_enchimento a abrir
#   |                   /
#   |__________________/                           k_livre       (≈ 0,43 kg/m)
#   +------------------+-----+-------------------> t
#                   t_abertura  t_abertura + t_enchimento
#
# - Antes da abertura:   k = k_livre
# - Durante o enchimento: k cresce em linha reta de k_livre até k_paraquedas
#                         (suposição simples: na realidade a área cresce de forma mais complicada)
# - Depois:              k = k_paraquedas
# - Com t_enchimento = 0 a passagem é instantânea (como na Etapa 4).
#
# Porque é que o enchimento importa?
# Com abertura instantânea, a força de arrasto passa de repente de ~mg para ~100 mg:
# o modelo prevê uma carga de ~100 g, que não acontece na realidade. Isto é um problema
# do MODELO. Além disso, um k muito grande torna o sistema muito "rápido" e o método de
# Euler precisa de um Δt pequeno para acompanhar (ver 3.). Isto é um problema do MÉTODO.
# O enchimento gradual resolve os dois ao mesmo tempo.


def k_no_instante(t, t_abertura, t_enchimento, k_livre, k_paraquedas):
    """Constante de arrasto no instante t (ver o esquema acima).
    t_abertura = None enquanto o paraquedas ainda não foi acionado."""
    if t_abertura is None:
        return k_livre
    if t_enchimento <= 0:
        return k_paraquedas
    f = min(1.0, (t - t_abertura) / t_enchimento)  # fração do enchimento: 0 → 1
    return k_livre + f * (k_paraquedas - k_livre)


def aceleracao(vx, vy, k, m):
    """Componentes da aceleração (y para cima), para a velocidade (vx, vy)."""
    v = (vx * vx + vy * vy) ** 0.5
    ax = -(k / m) * v * vx
    ay = -G - (k / m) * v * vy
    return ax, ay


# =============================================================================
# 3. MÉTODO NUMÉRICO (Euler)
# =============================================================================
# Em cada passo usamos a aceleração no início do intervalo:
#     v_{i+1} = v_i + a_i Δt          x_{i+1} = x_i + v_{x,i} Δt
#                                     y_{i+1} = y_i + v_{y,i} Δt
#
# Quando é que Δt é "pequeno"?  Perto da velocidade terminal, uma perturbação na
# velocidade é amortecida com um tempo característico  τ = m / (2 k v).
# O método de Euler só é estável se  Δt < 2τ = m / (k v);  e só não "passa por cima"
# do equilíbrio (oscilando) se  Δt < τ.
# Em queda livre τ ≈ 2 s (qualquer Δt razoável serve), mas no instante em que o
# paraquedas abre, com k ≈ 44 kg/m e v ≈ 43 m/s, τ ≈ 0,02 s!
# O painel de resultados mostra Δt/τ no pior instante do salto.


def simular(massa, y0, vx0, h_abertura, t_enchimento, diametro, dt):
    """Simula o salto completo, da saída do avião até ao solo.
    Devolve um dicionário com os arrays (t, x, y, vx, vy, k, carga) e um resumo."""
    k_livre = constante_arrasto(CD_CORPO, A_CORPO)
    k_paraq = constante_arrasto(CD_PARAQUEDAS, np.pi * diametro**2 / 4)

    n = int(T_MAX / dt) + 1
    t = [0.0]
    x = [0.0]
    y = [y0]
    vx = [vx0]
    vy = [0.0]
    ks = []
    carga = []
    t_abertura = None
    pior_razao = 0.0  # maior Δt/τ encontrado
    diverge = False

    for i in range(n - 1):
        # (a) o paraquedas é acionado quando se passa a altitude de abertura
        if t_abertura is None and y[i] <= h_abertura:
            t_abertura = t[i]

        # (b) modelo físico: k neste instante e aceleração
        k = k_no_instante(t[i], t_abertura, t_enchimento, k_livre, k_paraq)
        ax, ay = aceleracao(vx[i], vy[i], k, massa)

        # (c) grandezas para análise (não entram na simulação)
        v = (vx[i] ** 2 + vy[i] ** 2) ** 0.5
        ks.append(k)
        carga.append(k * v * v / (massa * G))  # força do arrasto em "g"
        if v > 0:
            pior_razao = max(pior_razao, dt / (massa / (2 * k * v)))

        # (d) passo de Euler
        vx.append(vx[i] + ax * dt)
        vy.append(vy[i] + ay * dt)
        x.append(x[i] + vx[i] * dt)
        y.append(y[i] + vy[i] * dt)
        t.append(t[i] + dt)

        # (e) critérios de paragem
        if abs(vy[-1]) > 1e4 or abs(vx[-1]) > 1e4:  # a simulação "explodiu"
            diverge = True
            break
        if y[-1] <= 0:  # chegou ao solo
            break

    ks.append(ks[-1])
    carga.append(carga[-1])
    r = {
        nome: np.array(val)
        for nome, val in dict(t=t, x=x, y=y, vx=vx, vy=vy, k=ks, carga=carga).items()
    }
    r.update(
        t_abertura=t_abertura,
        diverge=diverge,
        pior_razao=pior_razao,
        k_livre=k_livre,
        k_paraq=k_paraq,
        vt_livre=np.sqrt(massa * G / k_livre),
        vt_paraq=np.sqrt(massa * G / k_paraq),
    )
    return r


def texto_resumo(r):
    """Texto do painel de resultados."""
    linhas = [
        f"k livre     {r['k_livre']:5.2f} kg/m → v_t = {r['vt_livre']:.1f} m/s",
        f"k paraquedas {r['k_paraq']:4.1f} kg/m → v_t = {r['vt_paraq']:.2f} m/s",
        "",
    ]
    if r["diverge"]:
        linhas += [
            f"A SIMULAÇÃO DIVERGIU (t = {r['t'][-1]:.1f} s)",
            "→ reduza o Δt ou aumente",
            "  o tempo de enchimento",
        ]
    else:
        v_ater = np.hypot(r["vx"][-1], r["vy"][-1])
        sobe = r["vy"].max() > 1e-9 and r["t_abertura"] is not None
        linhas += [
            f"duração do salto  {r['t'][-1]:7.1f} s",
            f"queda livre       {r['t_abertura'] or r['t'][-1]:7.1f} s",
            f"aterragem         {v_ater:7.2f} m/s",
            f"                  {v_ater * 3.6:7.1f} km/h",
            f"deriva horizontal {r['x'][-1]:7.0f} m",
            f"carga máxima      {r['carga'].max():7.1f} g",
        ]
        if sobe:
            linhas += [
                "",
                "ATENÇÃO: v_y > 0, o paraquedista",
                "'sobe': é um artefacto numérico!",
            ]
    estado = (
        "estável"
        if r["pior_razao"] < 1
        else ("oscila" if r["pior_razao"] < 2 else "instável")
    )
    linhas += [
        "",
        f"pior Δt/τ = {r['pior_razao']:.2f}  → {estado}",
        "(< 1 bom; 1–2 oscila; > 2 pode divergir)",
    ]
    return "\n".join(linhas)


# =============================================================================
# 4. INTERFACE
# =============================================================================
def main():
    fig = plt.figure(figsize=(14, 8))
    fig.canvas.manager.set_window_title("MCSF — Simulador do salto de paraquedas")

    ax_traj = fig.add_axes([0.05, 0.08, 0.30, 0.84])
    ax_vel = fig.add_axes([0.42, 0.56, 0.30, 0.36])
    ax_carga = fig.add_axes([0.42, 0.08, 0.30, 0.36])
    ax_txt = fig.add_axes([0.755, 0.03, 0.24, 0.32])
    ax_txt.axis("off")

    # --- controlos -----------------------------------------------------------
    controlos = {}
    especificacao = [  # nome, rótulo, mínimo, máximo, passo
        ("massa", "massa (kg)", 50, 120, 1),
        ("y0", "altitude saída (m)", 1000, 4500, 50),
        ("vx0", "vel. avião (m/s)", 0, 80, 1),
        ("h_abertura", "altitude abertura (m)", 200, 2500, 50),
        ("t_enchimento", "enchimento (s)", 0, 6, 0.1),
        ("diametro", "diâmetro calote (m)", 4, 15, 0.1),
    ]
    for j, (nome, rotulo, vmin, vmax, passo) in enumerate(especificacao):
        eixo = fig.add_axes([0.85, 0.90 - j * 0.06, 0.12, 0.03])
        controlos[nome] = Slider(
            eixo, rotulo, vmin, vmax, valinit=INICIAIS[nome], valstep=passo
        )
    eixo = fig.add_axes([0.85, 0.90 - 6 * 0.06, 0.12, 0.03])
    # Δt escolhe-se entre valores fixos: o controlo dá a posição na lista PASSOS_DT
    controlos["dt"] = Slider(
        eixo,
        "Δt (s)",
        0,
        len(PASSOS_DT) - 1,
        valinit=PASSOS_DT.index(INICIAIS["dt"]),
        valstep=1,
    )

    bt_ref = Button(fig.add_axes([0.78, 0.40, 0.10, 0.045]), "Fixar referência")
    bt_repor = Button(fig.add_axes([0.89, 0.40, 0.08, 0.045]), "Repor")

    referencia = {"r": None}

    def desenhar(_=None):
        p = {nome: s.val for nome, s in controlos.items()}
        p["dt"] = PASSOS_DT[int(p["dt"])]
        controlos["dt"].valtext.set_text(f"{p['dt']:g}")
        r = simular(**p)
        for ax in (ax_traj, ax_vel, ax_carga):
            ax.clear()
            ax.grid(alpha=0.3)

        # referência (a cinzento)
        ref = referencia["r"]
        if ref is not None:
            ax_traj.plot(ref["x"], ref["y"], color="0.75", lw=2)
            ax_vel.plot(ref["t"], np.hypot(ref["vx"], ref["vy"]), color="0.75", lw=2)
            ax_carga.plot(ref["t"], ref["carga"], color="0.75", lw=2)

        aberto = r["k"] > r["k_livre"]
        # trajetória: azul em queda livre, laranja com o paraquedas
        ax_traj.plot(
            r["x"][~aberto],
            r["y"][~aberto],
            color="tab:blue",
            lw=2,
            label="queda livre",
        )
        ax_traj.plot(
            r["x"][aberto], r["y"][aberto], color="tab:orange", lw=2, label="paraquedas"
        )
        ax_traj.axhline(p["h_abertura"], color="tab:orange", ls=":", lw=1)
        ax_traj.plot(r["x"][-1], max(r["y"][-1], 0), "kv", ms=8)
        ax_traj.set_xlabel("x (m)")
        ax_traj.set_ylabel("altitude y (m)")
        ax_traj.set_title("Trajetória")
        ax_traj.legend(loc="upper right")
        ax_traj.set_ylim(bottom=0)

        # velocidades
        ax_vel.plot(r["t"], np.hypot(r["vx"], r["vy"]), color="k", lw=2, label="|v|")
        ax_vel.plot(r["t"], r["vx"], color="tab:green", lw=1.2, label="v_x")
        ax_vel.plot(
            r["t"], -r["vy"], color="tab:purple", lw=1.2, label="−v_y (descida)"
        )
        for vt in (r["vt_livre"], r["vt_paraq"]):
            ax_vel.axhline(vt, color="0.4", ls="--", lw=0.8)
        ax_vel.set_ylabel("m/s")
        ax_vel.set_title("Velocidade (tracejado: velocidades terminais)")
        ax_vel.legend(loc="upper right", fontsize=8)
        if not r["diverge"]:
            ax_vel.set_ylim(
                min(-5, (-r["vy"]).min() - 2), max(r["vx"].max(), r["vt_livre"]) * 1.15
            )

        # carga
        ax_carga.plot(r["t"], r["carga"], color="tab:red", lw=1.5)
        ax_carga.set_xlabel("t (s)")
        ax_carga.set_ylabel("carga (g)")
        ax_carga.set_title("Força do arrasto, em múltiplos do peso")
        if r["t_abertura"] is not None and not r["diverge"]:
            ax_carga.set_xlim(
                r["t_abertura"] - 5, r["t_abertura"] + 15
            )  # zoom na abertura

        ax_txt.clear()
        ax_txt.axis("off")
        ax_txt.text(0, 1, texto_resumo(r), va="top", family="monospace", fontsize=9)
        desenhar.ultimo = r
        fig.canvas.draw_idle()

    def fixar(_):
        referencia["r"] = desenhar.ultimo
        desenhar()

    def repor(_):
        referencia["r"] = None
        for s in controlos.values():
            s.reset()  # cada reset chama desenhar(); no fim fica tudo atualizado

    for s in controlos.values():
        s.on_changed(desenhar)
    bt_ref.on_clicked(fixar)
    bt_repor.on_clicked(repor)

    desenhar()
    fig._controlos = (controlos, bt_ref, bt_repor)  # manter referências vivas
    return fig


if __name__ == "__main__":
    main()
    plt.show()
