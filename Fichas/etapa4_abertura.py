"""
MCSF — Aula P05, Etapa 4: o salto completo.

Saída do avião a 3000 m (com a velocidade do avião, 50 m/s) e abertura do paraquedas
à altitude H_ABERTURA. Quando o paraquedas abre, a constante de arrasto passa de
K_LIVRE para K_PARAQUEDAS (abertura instantânea).
y é a ALTITUDE e aponta PARA CIMA, como na etapa 2.
"""

import numpy as np
from ferramentas import K_LIVRE, K_PARAQUEDAS, animar, grafico
from etapa2_saida_aviao import aceleracao

H_ABERTURA = 900.0  # altitude de abertura [m]
DT = 0.01  # passo de tempo [s] (não alterar nesta etapa)


def coef_arrasto(y, h_abertura=H_ABERTURA):
    """Constante de arrasto à altitude y: queda livre acima de h_abertura, paraquedas abaixo."""
    # TODO: complete com K_LIVRE acima da altitude de abertura e K_PARAQUEDAS abaixo
    if y > h_abertura:
        k = K_LIVRE
    else:
        k = K_PARAQUEDAS
    return k


def simular_salto(
    dt=DT, h_abertura=H_ABERTURA, x0=0.0, y0=3000.0, vx0=50.0, vy0=0.0, t_max=600.0
):
    """Simula o salto completo até ao solo. Devolve t, x, y, vx, vy e 'aberto' (True com o paraquedas aberto)."""
    n = int(round(t_max / dt)) + 1
    t = np.zeros(n)
    x = np.zeros(n)
    y = np.zeros(n)
    vx = np.zeros(n)
    vy = np.zeros(n)
    aberto = np.zeros(n, dtype=bool)
    x[0], y[0], vx[0], vy[0] = x0, y0, vx0, vy0
    for i in range(n - 1):
        k = coef_arrasto(y[i], h_abertura)
        aberto[i] = k == K_PARAQUEDAS
        ax, ay = aceleracao(vx[i], vy[i], k)  # a mesma função da etapa 2
        vx[i + 1] = vx[i] + ax * dt
        vy[i + 1] = vy[i] + ay * dt
        x[i + 1] = x[i] + vx[i] * dt
        y[i + 1] = y[i] + vy[i] * dt
        t[i + 1] = t[i] + dt
        if y[i + 1] <= 0:  # chegou ao solo: cortar os arrays
            aberto[i + 1] = aberto[i]
            s = slice(0, i + 2)
            return t[s], x[s], y[s], vx[s], vy[s], aberto[s]
    return t, x, y, vx, vy, aberto


if __name__ == "__main__":
    t, x, y, vx, vy, aberto = simular_salto()

    # TODO: determine o instante de abertura do paraquedas e a duração do salto
    t_ab = t[np.argmax(aberto)]  # primeiro instante com o paraquedas aberto
    duracao = t[-1] # o último instante de tempo será o momento em que chega ao solo
    v_aterragem = np.hypot(vx[-1], vy[-1])
    deriva = x[-1] - x[0]

    print(
        f"Abertura aos {t_ab:.1f} s (queda livre) | com paraquedas: {duracao - t_ab:.1f} s | total: {duracao:.1f} s"
    )
    print(
        f"Velocidade de aterragem: {v_aterragem:.2f} m/s  ({v_aterragem * 3.6:.1f} km/h)"
    )
    print(f"Deriva horizontal: {deriva:.0f} m")

    grafico(
        t,
        np.hypot(vx, vy),
        legendas=["|v| (m/s)"],
        ylabel="m/s",
        titulo="Etapa 4: o salto completo",
    )
    animar(t, x, y, vx, vy, ritmo=15.0, aberto=aberto)
