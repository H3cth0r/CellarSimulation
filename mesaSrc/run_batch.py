import mesa as ms
from Models import *
from Agents import *
import pandas as pd
import matplotlib.pyplot as plt

params = {"nBoxes":12, "negotiatorModel": True}
results = ms.batch_run(
    CellarModel,
    parameters=params,
    iterations=10,
    max_steps=125,
    number_processes=1,
    data_collection_period=1,
    display_progress=False)

# valor esperado o esperanza matemática

df = pd.DataFrame(results)
df.set_index("Step", inplace=True)
df.groupby("iteration")["Deactivated Robots"].plot(legend=False, ylabel="Deactivated robots")
plt.show()

deac_df = pd.DataFrame()
remBox_df = pd.DataFrame()
energy_df = pd.DataFrame()
for name, group in df.groupby('iteration'):
    deac = group[["Deactivated Robots"]]
    deac.rename({'Deactivated Robots':('DR' + str(name+1))})
    deac_df = pd.concat([deac_df, deac], axis=1)

    remBox = group[["Remaining Boxes"]]
    remBox.rename({'Remaining Boxes':('RB' + str(name+1))})
    remBox_df = pd.concat([remBox_df, remBox], axis=1)
    
    energy = group[["Energy Used"]]
    energy.rename({'Energy Used':('EU' + str(name+1))})
    energy_df = pd.concat([energy_df, energy], axis=1)

deac_df.mean(axis=1).plot(ylabel="Deactivated robots")
plt.show()

deactRobMean = df.groupby("iteration")["Deactivated Robots"].mean().mean()
print(f"Deactivated Robots mean for negotiator model (Valor esperado): {deactRobMean}")

df.groupby("iteration")["Remaining Boxes"].plot(legend=False, ylabel="Remaining boxes")
plt.show()

remBox_df.mean(axis=1).plot(ylabel="Remaining boxes")
plt.show()

remainingBoxesMean = remBox_df.iloc[-1].mean()
print(f"Remaining Boxes mean for negotiator model (Valor esperado): {remainingBoxesMean}")

df.groupby("iteration")["Energy Used"].plot(legend=False, ylabel="Energy used")
plt.show()

energy_df.mean(axis=1).plot(ylabel="Energy used")
plt.show()

energyUsedMean = energy_df.iloc[-1].mean()
print(f"Energy used mean for negotiator model (Valor esperado): {energyUsedMean}")

"""================================="""

params = {"nBoxes":12, "negotiatorModel": False}
results = ms.batch_run(
    CellarModel,
    parameters=params,
    iterations=10,
    max_steps=125,
    number_processes=1,
    data_collection_period=1,
    display_progress=False)

# valor esperado o esperanza matemática

df = pd.DataFrame(results)
df.set_index("Step", inplace=True)
#df.groupby("iteration")["Deactivated Robots"].plot(legend=False, ylabel="Deactivated robots")
#plt.show()

deac_df = pd.DataFrame()
remBox_df = pd.DataFrame()
energy_df = pd.DataFrame()
for name, group in df.groupby('iteration'):
    deac = group[["Deactivated Robots"]]
    deac.rename({'Deactivated Robots':('DR' + str(name+1))})
    deac_df = pd.concat([deac_df, deac], axis=1)

    remBox = group[["Remaining Boxes"]]
    remBox.rename({'Remaining Boxes':('RB' + str(name+1))})
    remBox_df = pd.concat([remBox_df, remBox], axis=1)
    
    energy = group[["Energy Used"]]
    energy.rename({'Energy Used':('EU' + str(name+1))})
    energy_df = pd.concat([energy_df, energy], axis=1)

#deac_df.mean(axis=1).plot(ylabel="Deactivated robots")
#plt.show()

deactRobMean = df.groupby("iteration")["Deactivated Robots"].mean().mean()
print(f"Deactivated Robots mean for random model (Valor esperado): {deactRobMean}")

df.groupby("iteration")["Remaining Boxes"].plot(legend=False, ylabel="Remaining boxes")
plt.show()

remBox_df.mean(axis=1).plot(ylabel="Remaining boxes")
plt.show()

remainingBoxesMean = remBox_df.iloc[-1].mean()
print(f"Remaining Boxes mean for random model (Valor esperado): {remainingBoxesMean}")

df.groupby("iteration")["Energy Used"].plot(legend=False, ylabel="Energy used")
plt.show()

energy_df.mean(axis=1).plot(ylabel="Energy used")
plt.show()

energyUsedMean = energy_df.iloc[-1].mean()
print(f"Energy used mean for random model (Valor esperado): {energyUsedMean}")