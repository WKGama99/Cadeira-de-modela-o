import math 
from pint import UnitRegistry 

ureg = UnitRegistry()

r = 1 * ureg.meter  
delta_P = 1 * ureg.pascal 
eta = 1 * ureg.pascal * ureg.second 
L = 1 * ureg.meter

Q_calculado = (math.pi * (r**4) * delta_P) / (8 * eta* L)
Q_espeardo = 1 * (ureg.meter ** 3 / ureg.second)
Q_calc_base = Q_calculado.to_base_units()
Q_espeardo_base = Q_espeardo.to_base_units()

print(f"Unidades calculadas (Lado Direito): {Q_calc_base.units}")
print(f"Unidades esperadas (Lado Esquerdo): {Q_espeardo_base.units}")

if Q_calculado.dimensionality == Q_espeardo.dimensionality:
    print("Sucesso! A equação é dimensionalmente coerente.")
else:
    print("Erro: As dimensões não coincidem.")