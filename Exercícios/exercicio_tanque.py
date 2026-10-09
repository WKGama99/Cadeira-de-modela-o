"""
exercicio_tanque.py
À procura do melhor Δt para estimar o caudal em t = 30 s.

Completa as linhas marcadas com  # <-- COMPLETA, pergunta a pergunta.
Podes correr o programa a qualquer momento: as perguntas ainda por completar
aparecem como "por completar" e não impedem as restantes de correr.
Corre com:  python exercicio_tanque.py
"""

import numpy as np
import matplotlib.pyplot as plt

A = 1.0  # área da base do tanque (m²)
TAU = 50.0  # constante do tubo (s)
T0 = 30  # instante em que queremos o caudal (s)

# ------------------------------------------------------------------ dados (já feito)
t, h_ideal, h_real = np.loadtxt("tanque_sensor.csv", delimiter=",", skiprows=1).T
i0 = np.where(t == T0)[0][0]  # posição (índice) da leitura de t = 30 s

print("Leituras em torno de t = 30 s:")
print("   t (s)   ideal (m)   real (m)")
for i in range(i0 - 5, i0 + 6):
    print(f"   {t[i]:4.0f}    {h_ideal[i]:.4f}      {h_real[i]:.4f}")


# ------------------------------------------------------------------ Pergunta 1
# Caudal de referência, pelo modelo laminar: Q = A h / TAU  (× 1000 para L/s)
Q_ref = (A * h_ideal[i0] / TAU) * 1000 # <-- COMPLETA (usa h_ideal[i0])

if Q_ref is None:
    print("\nPergunta 1: por completar")
else:
    print(f"\nPergunta 1: caudal de referência = {Q_ref:.2f} L/s")


# ------------------------------------------------------------------ função do caudal
def caudal_central(h, k):
    """Caudal (L/s) em t = 30 s, usando a leitura k posições ANTES e k posições DEPOIS
    de t = 30 s (que está na posição i0)."""
    h_antes = h[i0 - k]  # (exemplo: leitura k posições antes)
    h_depois = h[i0 + k]  # <-- COMPLETA
    t_antes = t[i0 - k]  # <-- COMPLETA
    t_depois = t[i0 + k]  # <-- COMPLETA
    dhdt = (h_depois - h_antes) / (
        t_depois - t_antes
    )  # <-- COMPLETA (diferença central)
    Q = -A * dhdt * 1000 # <-- COMPLETA (Q = -A dh/dt, em L/s)
    return Q


def erro(Q):
    """Erro (em L/s) de uma estimativa do caudal, em relação à referência."""
    return abs(Q_ref - Q) # <-- COMPLETA (valor absoluto da diferença)


funcoes_prontas = (
    Q_ref is not None
    and caudal_central(h_ideal, 1) is not None
    and erro(0.0) is not None
)


# ------------------------------------------------------------------ Perguntas 2 e 3
print("\nPerguntas 2 e 3:")
if not funcoes_prontas:
    print("  por completar (Pergunta 1 e funções caudal_central e erro)")
else:
    print("  Δt (s)  leituras usadas   Q ideal   erro  |  Q real   erro")
    for k in [1, 2, 5, 10, 20]:
        Qi = caudal_central(h_ideal, k)  # <-- COMPLETA (caudal com o sensor ideal)
        Qr = caudal_central(h_real, k)  # <-- COMPLETA (caudal com o sensor real)
        if Qi is None or Qr is None:
            print("  por completar (Qi e Qr)")
            break
        print(
            f"  {k:4d}    {t[i0-k]:2.0f} s e {t[i0+k]:2.0f} s    "
            f"{Qi:6.2f}  {erro(Qi):6.3f} |  {Qr:6.2f}  {erro(Qr):6.3f}"
        )


# ------------------------------------------------------------------ Pergunta 4
print("\nPergunta 4:")
ks = np.arange(1, 31)  # todos os Δt possíveis, de 1 a 30 s
erros_ideal = []
erros_real = []
if funcoes_prontas:
    for k in ks:
        pass  # <-- COMPLETA (2 linhas: acrescenta às listas
        #     o erro de cada sensor; usa .append)

melhor_k = None  # <-- COMPLETA (Δt com o menor erro do sensor
#     real; sugestão: ks[np.argmin(...)])

if len(erros_real) != len(ks):
    print("  por completar (listas de erros)")
else:
    if melhor_k is None:
        print("  melhor Δt: por completar")
    else:
        print(f"  melhor Δt com o sensor real = {melhor_k} s")
    plt.figure(figsize=(8, 5))
    plt.plot(ks, erros_ideal, "o-", label="sensor ideal")
    plt.plot(ks, erros_real, "s-", label="sensor real (erro de 1 mm)")
    plt.xlabel("Δt (s)")
    plt.ylabel("erro do caudal (L/s)")
    plt.title("Caudal em t = 30 s: erro em função de Δt")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------------ Pergunta 5
# Diferença entre os dois sensores, em milímetros, em todas as leituras
diferenca = None  # <-- COMPLETA (valor absoluto de
#     h_real - h_ideal, × 1000 para mm)
if diferenca is None:
    print("\nPergunta 5: por completar")
else:
    print(
        f"\nPergunta 5: os sensores diferem, em média, {np.mean(diferenca):.1f} mm "
        f"(no máximo {np.max(diferenca):.1f} mm)"
    )
