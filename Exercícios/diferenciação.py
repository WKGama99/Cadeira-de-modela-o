#%%
import numpy as np
x = [0.0, 0.049, 0.196, 0.441, 0.784, 1.225]
dt = 0.1
v = np.diff(x) / dt

print (v)

#%%
a = np.diff(v) / dt
print(a)
 
# %%
import numpy as np

t = [0.49, 1.47, 2.45, 3.43, 4.41]
d = 0.1
a = np.diff(t) / d
print("Aceleracoes (m/s^2):", np.round(a, 2))
# %%

# %%
