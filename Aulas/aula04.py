#%%
import numpy as np

#%%

t = np.array([0, 1, 2, 3, 4, 5])
f = t**2
df_exact = 2*t

print(t)
print(f)
print(df_exact)

# %%
dt = t[1] - t[0]

print(dt)
# %%
df_progressive = np.diff(f) / dt
df_progressive = (t[1:] - t[:-1]) / dt
print(df_progressive)

# %%
df_central = (f[2:] - f[:-2]) / (2*dt)
print(df_central)

#%%
print(df_exact)
print (np.gradient (f, dt))
# %%
