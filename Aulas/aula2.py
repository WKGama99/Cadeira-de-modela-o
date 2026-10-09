x = 1.1
y = 2.2

print(x+y)

#%% 
if x + y == 3.3: 



# %% 
eps = 1e-10 

z = x + y

if  (z - eps) < 3.3 :
    print("x + y is approximately 3.3")
else:
    print("x+y is not approximately 3.3")


# %%

from math import sqrt

for k in range (4, 17, 3):
    x = 10.0 ** k
    a = sqrt(x + 1) - sqrt(x)
    print("k =", k, "a =", a)



# %%
from math import sqrt 

for k in range(4, 17, 3):
    x = 10.0**k
    a = sqrt (x + 1) - sqrt(x) 
    b = 1 / (sqrt(x + 1) + sqrt(x))
    print(f"x = 1e{k:<2}   ingénua (a) = {a:.12e}  estável (b) = {b:.12e}")
# %%
from math import sqrt


x = 1e15
f1 = sqrt(x) * (sqrt(x + 1) - sqrt(x))
print(f"f = {f2:,15e}")

f2 = sqrt(x) / (sqrt(x + 1) + sqrt(x))
print(f"f - f2 = {f1-f2:.15e}")


# %%
h = 0.1
t = 0.0 

for n in range(1, 1_100_001):
    t += h
    if n in (10, 1_100, 100_000, 1_000_000):
        exato = n * h 
        print(
            f"n = {n:<9} t = {t:.15f}  n*h = {exato:.15f}   erro = {abs(t-exato):.3e}"
        ) 
        
# %%
