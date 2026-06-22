# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 14:47:37 2026

@author: Christine.ODonnell
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Import your data
df = pd.read_csv("Histograms_Input.csv")

# 2. Select only the columns you want to overlay
df_subset = df[['CompTox', 'NIST', 'Egg', 'Corn']]

# 3. Generate overlaid histograms
# Passing the whole dataframe tells Seaborn to treat it as "wide-form" 
# and plot each numeric column as a separate layer.
plt.figure(figsize=(3.33, 2), dpi=300)# fig size (in inches) and dpi
sns.histplot(data=df_subset, kde=True, alpha=0.5, palette="Paired", legend=False)
sns.despine(top= True, right= True, left= False, bottom=False)
#designate plot font and size
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams.update({'font.size': 12})


plt.xlabel("Mass Defect")
plt.ylabel("Number of Compounds")
plt.show()