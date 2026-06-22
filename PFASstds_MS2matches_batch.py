# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:09:58 2026

@author: Christine.ODonnell
"""

import pandas as pd
import os

# 1. Input and output file locations
folder_path = r'xxx'  #input folder location (replace xxx with your folder path)
ref_file = 'PFASstds.csv'
output_file = os.path.join(r'xxx') #output folder location (replace xxx with your folder path)

# Reference and Data columns
ref_col1, ref_col2 = 'm/z', 'RT' #ensure these match the column headers in the ref_file
data_col1, data_col2 = 'Mass [m/z]', 'Start [min]' #these are the column headers output from the IEomics software for each iterative MS2 file

# Tolerances
masserror = 0.005 #desired mass error in Da
RTrange = 0.3 #desired RT window in min

# 2. Load reference standards once
ref_df = pd.read_csv(ref_file)

all_final_matches = []

# 3. Iterate through every CSV file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv') and filename != ref_file and filename != output_file:
        file_path = os.path.join(folder_path, filename)
        data_df = pd.read_csv(file_path)
        
        file_matches = []
        
        # Iterate through current file data
        for i, d_row in data_df.iterrows():
            mask = (
                (ref_df[ref_col1] - d_row[data_col1]).abs() <= masserror
            ) & (
                (ref_df[ref_col2] - d_row[data_col2]).abs() <= RTrange
            )
            
            matches = ref_df[mask].copy()
            
            if not matches.empty:
                # ADD DATA FILE INFO: Store the actual values that caused the match
                    matches['matched_data_mz'] = d_row[data_col1]
                    matches['matched_data_RT'] = d_row[data_col2]
                    matches['source_file'] = filename
                    file_matches.append(matches)
        
        if file_matches:
            # Consolidate matches for this specific file
            combined_file_df = pd.concat(file_matches, ignore_index=True)
            all_final_matches.append(combined_file_df)
            print(f"Processed {filename}: Found {len(combined_file_df)} matches.")
        else:
            print(f"Processed {filename}: No matches found.")

# 4. Consolidate all results into one final CSV
if all_final_matches:
    final_results_df = pd.concat(all_final_matches, ignore_index=True)
    final_results_df.to_csv(output_file, index=False)
    print(f"\nSuccess! Found {len(final_results_df)} total matches across all files.")
else:
    print("\nNo matches found in any of the files.")