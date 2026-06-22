# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:35:40 2026

@author: Christine.ODonnell
"""

import pandas as pd
import numpy as np

# 1. Load Data
df = pd.read_csv('Histograms_Input.csv')

# Clean column names (removes hidden spaces like ' Source ')
df.columns = df.columns.str.strip()

# 2. Extract and Combine (Change these strings to match your CSV headers); add or delete strings to consider different numbers of distributions
targets = pd.concat([df['CompTox'], df['NIST']]).dropna() # distributions you want to include
excludes = pd.concat([df['Egg'], df['Corn']]).dropna() # distributions you want to exclude

# 3. Define search space (100 potential points across the data range)
all_data = pd.concat([targets, excludes])
potential_cuts = np.percentile(all_data, np.linspace(0, 100, 100))

best_score = -float('inf')
best_range = (None, None)

# 4. Iterate to find the best window [low, high]
for i, low in enumerate(potential_cuts):
    for high in potential_cuts[i+1:]:
        # Calculate coverage percentages
        t_cov = ((targets >= low) & (targets <= high)).mean()
        e_cov = ((excludes >= low) & (excludes <= high)).mean()
        
        # Maximize gap: Target Coverage - Exclude Coverage
        score = t_cov - e_cov
        
        if score > best_score:
            best_score = score
            best_range = (low, high)

# 5. Print Results
print("-" * 30)
print(f"Optimal X-Axis Range: {best_range[0]:.4f} to {best_range[1]:.4f}")
print(f"Maximum Difference: {best_score:.2%}")
print("-" * 30)
print(f"Targets Captured: {((targets >= best_range[0]) & (targets <= best_range[1])).mean():.2%}")
print(f"Excludes Captured: {((excludes >= best_range[0]) & (excludes <= best_range[1])).mean():.2%}")