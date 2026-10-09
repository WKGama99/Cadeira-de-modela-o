
import numpy as np

file = "sunspots.txt"

dados = np.loadtxt(file)



#%%
print("estou a imprimir dados", dados)



#%% 

meses = dados [: , 0]
manchas_solares = dados[: , 1]

#%%
print(f"N_months: {len(meses)}, N_sunspots: {len(manchas_solares)}")

       #%%
maximo_atual = -1


for i in range(len(meses)):
    if manchas_solares [i] > maximo_atual:
        maximo_atual = manchas_solares[i]

        print("Maximum number of sunspots:", {maximo_atual})

        #%% 
        manchas_solares.max()


#%% 
minimo_atual = 10**10

# for i in range(len(meses));
    #if manchas_solares[i] < minimo_atual; 