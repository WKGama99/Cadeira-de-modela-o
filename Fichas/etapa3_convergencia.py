"""
MCSF — Aula P05, Etapa 3: o Δt importa?

Usa a simulação da etapa 1 (queda vertical) e compara com a solução exata em t = 5 s,
para vários passos Δt. Se o erro cair para metade quando Δt cai para metade,
o método é de 1.ª ordem (como a diferença progressiva da TP04).
"""

import numpy as np
from ferramentas import v_exata
from etapa1_queda_vertical import simular, K

T_COMPARAR = 5.0
passos = [1.0, 0.5, 0.25, 0.125, 0.0625]

if __name__ == "__main__":
    erros = []
    print("   Δt (s)     v(5 s)    exata     erro      razão")
    for dt in passos:
        # TODO: simular até T_COMPARAR e calcular o erro em t = 5 s
        t,v ,a ,d = simular(dt, T_COMPARAR, K)
        # TODO: substituir v_final pela verdadeira
        v_final = v[-1]
        erro = v_final - v_exata(T_COMPARAR, k=K)
        razao = erros[-1] / erro if erros else np.nan
        erros.append(erro)
        print(
            f"  {dt:7.4f}   {v_final:8.4f}  {v_exata(T_COMPARAR, k=K):8.4f}  {erro:+.4f}   {razao:6.2f}"
        )
