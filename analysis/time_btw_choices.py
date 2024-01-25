import os, choix, pdb, random
import networkx as nx
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from itertools import combinations, permutations

import matplotlib.pyplot as plt # BB

# Older (Dropbpx MGH)
# WKDIR='couchdb_results/Opthamology/RIM-ONE/compare_results_01_03_2023'

# Linux Tower 1
WKDIR="/sddata/app_or_generated_data/Image-Comparator-Analysis/raw_annotations/opthamology_rim-one/"

# Old
# DATA_OUT="/projects/Image-Comparator-Analysis/analysis"

# 01_24_2024
DATA_OUT="/sddata/app_or_generated_data/Image-Comparator-Analysis/analysis/some_choix_and_elo_ranks_01_03_2023/some_tweaks_01_24_2024"

# Linux Tower 1
images = pd.read_csv(os.path.join("/sddata/app_or_generated_data/Image-Comparator-Analysis/raw_annotations/opthamology_rim-one/images_opthamology_rim-one_app_images_key.csv")) # get actual images if needed
images.app_image_id.max() # 158
images.app_image_id.min() # 1

# Compare
# WKDIR=os.path.join(WKDIR,'opthamology_rim-one_50_CompareList')
results_Lazcano = pd.read_csv(os.path.join(WKDIR, "Lazcano_compare_results_01_03_2023.csv"))
results_Alryalat = pd.read_csv(os.path.join(WKDIR, "Alryalat_compare_results_01_03_2023.csv"))
results_Seibold = pd.read_csv(os.path.join(WKDIR, "Seibold_compare_results_01_03_2023.csv"))
results_Malik = pd.read_csv(os.path.join(WKDIR, "Malik_compare_results_01_03_2023.csv"))
results_Ittoop = pd.read_csv(os.path.join(WKDIR, "Ittoop_compare_results_01_03_2023.csv"))

# Classify
# WKDIR=os.path.join(WKDIR,'opthamology_rim-one-10p-repeat_ClassifyList')
results_Lazcano = pd.read_csv(os.path.join(WKDIR, "Lazcano_classify_results_10_25_2022.csv"))
results_Seibold = pd.read_csv(os.path.join(WKDIR, "Seibold_classify_results_10_25_2022.csv"))
results_Malik = pd.read_csv(os.path.join(WKDIR, "Malik_classify_results_10_25_2022.csv"))
results_Ittoop = pd.read_csv(os.path.join(WKDIR, "Ittoop_classify_results_10_25_2022.csv"))



def time_bwt_choices(df):
    # pdb.set_trace()
    # Remove the extra information from date strings
    df['date_string'] = df['date'].str.slice(0,33)
    date_format = '%a %b %d %Y %H:%M:%S GMT%z'
    df['date'] = df['date_string'].apply(lambda x: pd.to_datetime(x, format=date_format))
    df_sorted = df.sort_values('task_idx')
    df_sorted['time_diff'] = df_sorted['date'].diff()
    return df_sorted





# Compare
time_Lazcano = time_bwt_choices(results_Lazcano)
time_Alryalat = time_bwt_choices(results_Alryalat)
time_Seibold = time_bwt_choices(results_Seibold)
time_Malik = time_bwt_choices(results_Malik)
time_Ittoop = time_bwt_choices(results_Ittoop)

compare_header = ['user', 'winner', 'image0', 'image1', 'image_name_0', 'image_name_1', 'date', 'time_diff']
abbr_time_Lazcano = time_Lazcano[compare_header]
abbr_time_Alryalat = time_Alryalat[compare_header]
abbr_time_Seibold = time_Seibold[compare_header]
abbr_time_Malik = time_Malik[compare_header]
abbr_time_Ittoop = time_Ittoop[compare_header]

abbr_time_Lazcano.to_csv(os.path.join(DATA_OUT, 'time_compare_Lazcano.csv'), index=None)
abbr_time_Alryalat.to_csv(os.path.join(DATA_OUT, 'time_compare_Alryalat.csv'), index=None)
abbr_time_Seibold.to_csv(os.path.join(DATA_OUT, 'time_compare_Seibold.csv'), index=None)
abbr_time_Malik.to_csv(os.path.join(DATA_OUT, 'time_compare_Malik.csv'), index=None)
abbr_time_Ittoop.to_csv(os.path.join(DATA_OUT, 'time_compare_Ittoop.csv'), index=None)


# Classify
time_Lazcano = time_bwt_choices(results_Lazcano)
# time_Alryalat = time_bwt_choices(results_Alryalat)
time_Seibold = time_bwt_choices(results_Seibold)
time_Malik = time_bwt_choices(results_Malik)
time_Ittoop = time_bwt_choices(results_Ittoop)

classify_header = ['user', 'image_name', 'diagnosis', 'date_string', 'time_diff']
abbr_time_Lazcano = time_Lazcano[classify_header]
# abbr_time_Alryalat = time_Alryalat[classify_header]
abbr_time_Seibold = time_Seibold[classify_header]
abbr_time_Malik = time_Malik[classify_header]
abbr_time_Ittoop = time_Ittoop[classify_header]

abbr_time_Lazcano.to_csv(os.path.join(DATA_OUT, 'time_classify_Lazcano.csv'), index=None)
# abbr_time_Alryalat.to_csv(os.path.join(DATA_OUT, 'time_classify_Alryalat.csv'), index=None)
abbr_time_Seibold.to_csv(os.path.join(DATA_OUT, 'time_classify_Seibold.csv'), index=None)
abbr_time_Malik.to_csv(os.path.join(DATA_OUT, 'time_classify_Malik.csv'), index=None)
abbr_time_Ittoop.to_csv(os.path.join(DATA_OUT, 'time_classify_Ittoop.csv'), index=None)