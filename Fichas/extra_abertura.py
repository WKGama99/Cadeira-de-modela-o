"""
MCSF — Aula P05, Extras: abertura gradual e altitude mínima de abertura.

Extra 1 (código fornecido): o paraquedas não abre de uma vez. A calote demora
t_enchimento segundos a encher e, durante esse tempo, k cresce em rampa
de K_LIVRE até K_PARAQUEDAS. Calculamos a carga (em g) sentida pelo paraquedista.

Extra 2: até que altitude se pode esperar para abrir o paraquedas e ainda aterrar
em segurança?

y é a ALTITUDE e aponta PARA CIMA, como nas Etapas 2 a 4.
"""

import numpy as np
from ferramentas import M, G, K_LIVRE, K_PARAQUEDAS
from etapa2_saida_aviao import aceleracao

DT = 0.01  # passo de tempo [s]
V_SEGURA = 5.5  # velocidade de aterragem máxima recomendada [m/s]


# ---------------------------------------------------------------------------
# Extra 1 — abertura gradual (código fornecido)
# ---------------------------------------------------------------------------
def coef_arrasto(t, t_abertura, t_enchimento):
    """Constante de arrasto no instante t.
    t_abertura   : instante em que o paraquedas foi acionado (None se ainda não abriu)
    t_enchimento : tempo que a calote demora a encher (0 = abertura instantânea)"""
    if t_abertura is None:  # ainda em queda livre
        return K_LIVRE
    if t_enchimento <= 0:  # abertura instantânea
        return K_PARAQUEDAS
    f = min(1.0, (t - t_abertura) / t_enchimento)  # fração cheia (0 a 1)
    return K_LIVRE + f * (K_PARAQUEDAS - K_LIVRE)


def simular_salto(
    h_abertura=900.0, t_enchimento=0.0, dt=DT, y0=3000.0, vx0=50.0, t_max=600.0
):
    """Simula o salto até ao solo. Devolve t, x, y, vx, vy e a carga (em g) em cada instante."""
    n = int(round(t_max / dt)) + 1
    t = np.zeros(n)
    x = np.zeros(n)
    y = np.zeros(n)
    vx = np.zeros(n)
    vy = np.zeros(n)
    carga = np.zeros(n)
    y[0], vx[0] = y0, vx0
    t_abertura = None
    for i in range(n - 1):
        if t_abertura is None and y[i] <= h_abertura:  # aciona o paraquedas
            t_abertura = t[i]
        k = coef_arrasto(t[i], t_abertura, t_enchimento)
        ax, ay = aceleracao(vx[i], vy[i], k)
        carga[i] = np.hypot(ax, ay + G) / G  # |a - g| / g  =  |F_a| / (m g)
        vx[i + 1] = vx[i] + ax * dt
        vy[i + 1] = vy[i] + ay * dt
        x[i + 1] = x[i] + vx[i] * dt
        y[i + 1] = y[i] + vy[i] * dt
        t[i + 1] = t[i] + dt
        if y[i + 1] <= 0:
            carga[i + 1] = carga[i]
            s = slice(0, i + 2)
            return t[s], x[s], y[s], vx[s], vy[s], carga[s]
    return t, x, y, vx, vy, carga


# ---------------------------------------------------------------------------
# Extra 2 — altitude mínima de abertura
# ---------------------------------------------------------------------------
def velocidade_aterragem(h_abertura, t_enchimento):
    """Módulo da velocidade quando o paraquedista chega ao solo."""
    t, x, y, vx, vy, carga = simular_salto(h_abertura, t_enchimento)
    return np.hypot(vx[-1], vy[-1])


def altitude_minima(t_enchimento, alturas):
    """Menor altitude de abertura (entre as 'alturas' testadas) com aterragem segura."""
    # TODO: percorrer as alturas por ordem crescente e devolver a primeira segura
    for h in alturas:
        if ...: # se a velocidade de aterragem estiver abaixo da velocidade segura; retorne a altura
            return h
    return np.nan


if __name__ == "__main__":
    print("Extra 1 — abertura a 900 m")
    print("  enchimento (s)   carga máx. (g)   aterragem (m/s)")
    for te in [0.0, 1.0, 2.5, 5.0]:
        t, x, y, vx, vy, carga = simular_salto(t_enchimento=te)
        print(f"  {te:10.1f}   {carga.max():14.1f}   {np.hypot(vx[-1], vy[-1]):15.2f}")

    t, x, y, vx, vy, carga = simular_salto(t_enchimento=2.5)

    print("\nExtra 2 — altitude mínima de abertura (aterragem a menos de 5,5 m/s)")
    alturas = np.arange(10.0, 301.0, 10.0)
    for te in [0.0, 1.0, 2.5, 5.0]:
        print(
            f"  enchimento {te:3.1f} s: abrir, no mínimo, a {altitude_minima(te, alturas):3.0f} m"
        )
