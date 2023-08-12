import os, sys, pdb, pandas as pd, numpy as np, math
from pathlib import Path
# from algorithms_and_utils.couch import couch_utils
# super hacky!
cwd = os.getcwd()
sys.path.insert(1, os.path.join(cwd, 'algorithms_and_utils'))
from couch import couch_utils

from dotenv import load_dotenv
from pycrumbs import tracked
 
load_dotenv()

DATA_DIR=os.environ["DATA_DIR"]
PROJECT_INPUT_DATA_DIR=os.environ["PROJECT_INPUT_DATA_DIR"]
PROJECT_DIR=os.environ["PROJECT_DIR"]
DNS=os.environ["DNS"]
IMAGES_DB=os.environ["IMAGES_DB"]
DB_PORT=os.environ["DB_PORT"]
DB_ADMIN_USER=os.environ["DB_ADMIN_USER"]
DB_ADMIN_PASS=os.environ["DB_ADMIN_PASS"]
ADMIN_PARTY=True if os.environ["ADMIN_PARTY"] == 'True' else False

c = couch_utils(DNS, DB_PORT, IMAGES_DB, DB_ADMIN_USER, DB_ADMIN_PASS, ADMIN_PARTY)

# Where I will put the csv(s)
OUT = os.path.join(PROJECT_DIR)

# Get Images #
# 05_25_2023
# images = c.get_images(key="opthamology_rim-one")
# 03_24_2023 - maybe
images = c.get_images(key="flicker_02_15_2023", v1=True)
# images.columns
# Index(['_id', '_rev', 'image_path', 'image_folder', 'origin', 'id', 'type', 'imageSetName', 'timeAdded'], dtype='object')

images['app_image_id'] = images['_id']
# images['app_image_id'] = images['app_image_id'].astype(int)
images['origin']
images.rename(columns={'origin':'image_name'}, inplace=True)
images['image_name']
images.columns
images.drop(columns=['_id', '_rev', 'type', 'timeAdded'], inplace=True)
# images.columns
# Index(['image_path', 'image_path_orig', 'image_type', 'image_name', 'id',
#        'imageSetName', 'app_image_id'],
#       dtype='object')

# @tracked(literal_directory=Path(OUT))
# def write_images_key():
#     images.to_csv(os.path.join(OUT, "flicker_02_15_2023.csv"), index=None)

# write_images_key()

# Flicker Results #
Saif_flicker_results = c.get_flicker_results("Saif", "flicker_02_15_2023_FlickerList", v1=True)
Galia_flicker_results = c.get_flicker_results("Galia", "flicker_02_15_2023_FlickerList", v1=True)
Jayashree_flicker_results = c.get_flicker_results("Jayashree", "flicker_02_15_2023_FlickerList", v1=True)

# annotator_results = {
#     "Saif_flicker_results": Saif_flicker_results,
#     "Galia_flicker_results": Galia_flicker_results,
#     "Jayashree_flicker_results": Jayashree_flicker_results,
#     }

Saif_flicker_results.columns
Saif_flicker_results.drop(['_id','_rev'], inplace=True, axis=1)
Saif_flicker_results.head()
Saif_flicker_results['img0_app_image_id'] = Saif_flicker_results['img0'].str.replace('http://image-comparator.eastus.cloudapp.azure.com:5991/image_comparator/image', '')
Saif_flicker_results['img1_app_image_id'] = Saif_flicker_results['img1'].str.replace('http://image-comparator.eastus.cloudapp.azure.com:5991/image_comparator/image', '')
header = ['user', 'type', 'date', 'image_name', 'img0', 'img1', 'diagnosis', 'justification', 'task', 'task_list_name', 'task_idx', 'img0_app_image_id', 'img1_app_image_id']
Saif_flicker_results = pd.merge(Saif_flicker_results, images[['app_image_id','image_name']], left_on="img0_app_image_id", right_on="app_image_id")[header]
header = ['user', 'type', 'date', 'image_name_img0', 'image_name_img1', 'img0', 'img1', 'diagnosis', 'justification', 'task', 'task_list_name', 'task_idx', 'img0_app_image_id', 'img1_app_image_id']
Saif_flicker_results = pd.merge(Saif_flicker_results, images[['app_image_id','image_name']], left_on="img1_app_image_id", right_on="app_image_id", suffixes=["_img0", "_img1"])[header]

Galia_flicker_results.columns
Galia_flicker_results.drop(['_id','_rev'], inplace=True, axis=1)
Galia_flicker_results.head()
Galia_flicker_results['img0_app_image_id'] = Galia_flicker_results['img0'].str.replace('http://image-comparator.eastus.cloudapp.azure.com:5991/image_comparator/image', '')
Galia_flicker_results['img1_app_image_id'] = Galia_flicker_results['img1'].str.replace('http://image-comparator.eastus.cloudapp.azure.com:5991/image_comparator/image', '')
header = ['user', 'type', 'date', 'image_name', 'img0', 'img1', 'diagnosis', 'justification', 'task', 'task_list_name', 'task_idx', 'img0_app_image_id', 'img1_app_image_id']
Galia_flicker_results = pd.merge(Galia_flicker_results, images[['app_image_id','image_name']], left_on="img0_app_image_id", right_on="app_image_id")[header]
header = ['user', 'type', 'date', 'image_name_img0', 'image_name_img1', 'img0', 'img1', 'diagnosis', 'justification', 'task', 'task_list_name', 'task_idx', 'img0_app_image_id', 'img1_app_image_id']
Galia_flicker_results = pd.merge(Galia_flicker_results, images[['app_image_id','image_name']], left_on="img1_app_image_id", right_on="app_image_id", suffixes=["_img0", "_img1"])[header]

Jayashree_flicker_results.columns
Jayashree_flicker_results.drop(['_id','_rev'], inplace=True, axis=1)
Jayashree_flicker_results.head()
Jayashree_flicker_results['img0_app_image_id'] = Jayashree_flicker_results['img0'].str.replace('http://image-comparator.eastus.cloudapp.azure.com:5991/image_comparator/image', '')
Jayashree_flicker_results['img1_app_image_id'] = Jayashree_flicker_results['img1'].str.replace('http://image-comparator.eastus.cloudapp.azure.com:5991/image_comparator/image', '')
header = ['user', 'type', 'date', 'image_name', 'img0', 'img1', 'diagnosis', 'justification', 'task', 'task_list_name', 'task_idx', 'img0_app_image_id', 'img1_app_image_id']
Jayashree_flicker_results = pd.merge(Jayashree_flicker_results, images[['app_image_id','image_name']], left_on="img0_app_image_id", right_on="app_image_id")[header]
header = ['user', 'type', 'date', 'image_name_img0', 'image_name_img1', 'img0', 'img1', 'diagnosis', 'justification', 'task', 'task_list_name', 'task_idx', 'img0_app_image_id', 'img1_app_image_id']
Jayashree_flicker_results = pd.merge(Jayashree_flicker_results, images[['app_image_id','image_name']], left_on="img1_app_image_id", right_on="app_image_id", suffixes=["_img0", "_img1"])[header]


Saif_flicker_results.to_csv(os.path.join(OUT, f"Saif_flicker_results_05_25_2023.csv"), index=None)
Galia_flicker_results.to_csv(os.path.join(OUT, f"Galia_flicker_results_05_25_2023.csv"), index=None)
Jayashree_flicker_results.to_csv(os.path.join(OUT, f"Jayashree_flicker_results_05_25_2023.csv"), index=None)
