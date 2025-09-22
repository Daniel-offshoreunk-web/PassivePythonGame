import pandas as pd
import numpy as np
import time

df = pd.DataFrame({
    "Cash": [0.0],
    "Cps": [0.0],
    "Cps Cost": [10],
    "Cm": [1],
    "Cm Cost": [100],
    "Cv": [1],
    "Cv_Cost": [100],
    "Last Online": [time.time()],
    "Luck": [1],
    "Username": ["DEVELOPER"],
    "Password": ["devpassword"]
    })
    
print("Saving...")
with open("GameMainFrame.csv", "w") as f:
    f.close()
df.to_csv('GameMainFrame.csv', index=False)
print("Saved!")
print(df)
