"""
MCSF — Aula P05, Etapa 1: queda vertical (1D) com o método de Euler.

Convenção: sentido positivo PARA BAIXO (como no exercício da aula TP).
  a_i     = g - (k/m) v_i²
  v_{i+1} = v_i + a_i Δt
  d_{i+1} = d_i + v_i Δt          (d = distância percorrida em queda)
"""


import numpy as np
from ferramentas import M, G, v_exata, grafico

K = 0.43  # constante de arrasto em queda livre [kg/m] (valor arredondado, como na TP)





def aceleracao(v):
    """Aceleração (positiva para baixo) quando a velocidade de queda é v."""
    a = G - (K/M) * v**2   # TODO: 2.ª lei de Newton: a = g - (k/m) v² (atenção: os valores de M e G já estão definidos)
    return a


def simular(dt, t_max, v0=0.0):
    """Simula a queda com o método de Euler. Devolve os arrays t, v, a, d."""
    n = int(round(t_max / dt)) + 1
    t = np.zeros(n)
    v = np.zeros(n)
    a = np.zeros(n)
    d = np.zeros(n)
    v[0] = v0
    for i in range(n - 1):
        a [i] = aceleracao(v[i]) 
        v [i+1] = v[i] + a[i] * dt
        d [i+1] = d[i] + v[i] * dt
        t [i+1] = t[i] + dt 
         # TODO: um passo de Euler (calcular a[i], depois v[i+1], d[i+1] e t[i+1])
        pass
    a[-1] = aceleracao(v[-1])
    return t, v, a, d


if __name__ == "__main__":
    # 1) Os primeiros passos devem coincidir com a tabela da aula TP (Δt = 1 s).
    t, v, a, d = simular(dt=1.0, t_max=3.0)
    print(" i   t (s)   v (m/s)   a (m/s²)   v exata")
    for i in range(len(t)):
        print(
            f"{i:2d}  {t[i]:5.1f}   {v[i]:7.2f}   {a[i]:7.2f}    {v_exata(t[i], k=K):7.2f}"
        )

    # 2) Uma simulação mais longa, com Δt = 0,1 s, comparada com a solução exata.
    t, v, a, d = simular(dt=0.1, t_max=30.0)
    vt = np.sqrt(M * G / K)
    print(f"\nv(30 s) = {v[-1]:.2f} m/s   |   v_t = sqrt(mg/k) = {vt:.2f} m/s")
    print(f"distância percorrida em 30 s: {d[-1]:.0f} m")
    grafico(
        t,
        v,
        v_exata(t, k=K),
        legendas=["Euler, Δt = 0,1 s", "solução exata"],
        ylabel="velocidade de queda (m/s)",
        titulo="Etapa 1: queda vertical",
    )
