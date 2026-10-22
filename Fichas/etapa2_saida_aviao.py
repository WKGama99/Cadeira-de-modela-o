"""
MCSF — Aula P05, Etapa 2: saída de um avião (2D) com o método de Euler.

ATENÇÃO: a partir daqui, y é a ALTITUDE e aponta PARA CIMA.
  F_a = -k |v| v         (oposta à velocidade)
  a_x = -(k/m) |v| v_x
  a_y = -g - (k/m) |v| v_y
"""

import numpy as np
from ferramentas import M, G, K_LIVRE, animar, trajetoria, grafico


def aceleracao(vx, vy, k):
    """Componentes da aceleração (y para cima) para a velocidade (vx, vy)."""
    v = np.sqrt(vx**2 + vy**2)
    ax = -(k/M) * v * vx # TODO: módulo da velocidade e as duas componentes da aceleração
    ay = -G - (k/M) * v * vy
    return ax, ay


def simular(dt, t_max, x0=0.0, y0=3000.0, vx0=50.0, vy0=0.0, k=K_LIVRE):
    """Simula a queda em 2D até t_max (ou até chegar ao solo). Devolve t, x, y, vx, vy."""
    n = int(round(t_max / dt)) + 1
    t = np.zeros(n)
    x = np.zeros(n)
    y = np.zeros(n)
    vx = np.zeros(n)
    vy = np.zeros(n)
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    for i in range(n - 1):
        ax, ay = aceleracao(vx[i], vy[i], k)
        vx[i+1] = vx[i] + ax * dt
        vy[i+1] = vy[i] + ay * dt
        x[i+1] = x[i] + vx[i] * dt
        y[i+1] = y[i] + vy[i] * dt
        t[i+1] = t[i] + dt
        # TODO: um passo de Euler para as duas componentes
        if t[i + 1] > 0 and y[i + 1] <= 0:  # chegou ao solo: cortar os arrays
            return t[: i + 2], x[: i + 2], y[: i + 2], vx[: i + 2], vy[: i + 2]
    return t, x, y, vx, vy


if __name__ == "__main__":
    DT = 0.01

    # Validação A: sem ar (k = 0) a trajetória tem de ser a parábola.
    t, x, y, vx, vy = simular(DT, 20.0, k=0.0)
    x_ex = 50 * t 
    y_ex = 3000 - 1/2 * G * t**2
    # TODO: posição exata sem ar, x(t) e y(t) (substituir a linha em baixo com as equações do enunciado)
    print(
        f"A) sem ar: maior erro em x = {np.abs(x - x_ex).max():.3f} m, em y = {np.abs(y - y_ex).max():.3f} m"
    )

    # Validação B: com vx0 = 0 tem de reproduzir a etapa 1 (agora com v_y negativa).
    from etapa1_queda_vertical import simular as simular_1d
    from etapa1_queda_vertical import K as K_1D

    t, x, y, vx, vy = simular(DT, 20.0, vx0=0.0, k=K_1D)  # mesmo k da etapa 1
    t1, v1, _, _ = simular_1d(DT, 20.0)
    print(
        f"B) vx0 = 0: maior diferença para a etapa 1 = {np.abs(-vy[:len(v1)] - v1[:len(vy)]).max():.2e} m/s"
    )

    # Validação C: ao fim de algum tempo, v_x → 0 e |v| → v_t.
    t, x, y, vx, vy = simular(DT, 40.0)
    vt = np.sqrt(M * G / K_LIVRE)
    print(
        f"C) t = 40s: vx = {vx[-1]:.3f} m/s, |v| = {np.hypot(vx[-1], vy[-1]):.2f} m/s, v_t = {vt:.2f} m/s"
    )
    print(f"   deriva horizontal ao fim de 40 s: {x[-1]:.0f} m")

    grafico(
        t,
        np.hypot(vx, vy),
        vx,
        -vy,
        legendas=["|v|", "v_x", "-v_y"],
        ylabel="m/s",
        titulo="Etapa 2: componentes da velocidade",
    )
    animar(t, x, y, vx, vy, ritmo=5.0)
