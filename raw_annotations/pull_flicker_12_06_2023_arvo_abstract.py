import os, sys, pdb, pandas as pd, numpy as np, math
import importlib

from pathlib import Path
# from algorithms_and_utils.couch import couch_utils
# super hacky!
cwd = os.getcwd()
sys.path.insert(1, os.path.join(cwd, 'algorithms_and_utils'))
import couch
importlib.reload(couch) # helper

from dotenv import load_dotenv
from pycrumbs import tracked

load_dotenv(".env_pull")

DATA_DIR=os.environ["DATA_DIR"]
PROJECT_DIR=os.environ["PROJECT_DIR"]
DNS=os.environ["DNS"]
IMAGES_DB=os.environ["IMAGES_DB"]
DB_PORT=os.environ["DB_PORT"]
DB_ADMIN_USER=os.environ["DB_ADMIN_USER"]
DB_ADMIN_PASS=os.environ["DB_ADMIN_PASS"]
ADMIN_PARTY=True if os.environ["ADMIN_PARTY"] == 'True' else False

c = couch.couch_utils(DNS, DB_PORT, IMAGES_DB, DB_ADMIN_USER, DB_ADMIN_PASS, ADMIN_PARTY)

# Where I will put the csv(s)
OUT = os.path.join(PROJECT_DIR)

# Get Images #
# 03_24_2023 - maybe but updated on 05_2_2023
images = c.get_images(key="v2_12_1_23")
# images.columns
# Index(['_id', '_rev', 'image_path', 'image_folder', 'origin', 'id', 'type', 'imageSetName', 'timeAdded'], dtype='object')

images['app_image_id'] = images['_id']
# images['origin']
images.rename(columns={'origin':'image_name'}, inplace=True)
# images['image_name']
images.columns
images.drop(columns=['_id', '_rev', 'type', 'timeAdded'], inplace=True)
# images.columns
# Index(['image_path', 'image_folder', 'image_name', 'imageSetName', 'app_image_id'], dtype='object')

# @tracked(literal_directory=Path(OUT))
def write_images_key():
    # images.to_csv(os.path.join(OUT, "opthamology_rim-one.csv"), index=None)
    images.to_csv(os.path.join(OUT, "app_image_key.csv"), index=None)

write_images_key()

# Flicker Results #
steve_flicker_results = c.get_flicker_results("mcnamast", "v2_12_1_23-flicker-0")
galia_flicker_results = c.get_flicker_results("gdeitz", "v2_12_1_23-flicker-0")
stephanie_flicker_results = c.get_flicker_results("swangyu", "v2_12_1_23-flicker-0")

# ---
steve_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose CDR Desc',
#        'Registration Quality Assessment', 'image 1 opacity', 'image 2 opacity',
#        'fade between images'],
#       dtype='object')

steve_flicker_results['_id'] = steve_flicker_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
steve_flicker_results['_id'] = steve_flicker_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = steve_flicker_results['list_name'].iloc[0].replace('-flicker-0','') + "_"
task = steve_flicker_results['taskid'].iloc[0]

steve_flicker_results['_id'].iloc[0] # check the strip

steve_flicker_results[['delete_me','image_1_id','image_2_id']] = steve_flicker_results['_id'].str.split(image_set, expand=True)
steve_flicker_results.drop(columns=["delete_me", "_id"], inplace=True)
steve_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose CDR Desc',
#        'Registration Quality Assessment', 'image 1 opacity', 'image 2 opacity',
#        'fade between images', 'image_1_id', 'image_2_id'],
#       dtype='object')

steve_flicker_results.to_csv(os.path.join(OUT, f"steve_{task}.csv"), index=None)

# ---
galia_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose CDR Desc',
#        'Registration Quality Assessment', 'image 1 opacity', 'image 2 opacity',
#        'fade between images'],
#       dtype='object')

galia_flicker_results['_id'] = galia_flicker_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
galia_flicker_results['_id'] = galia_flicker_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = galia_flicker_results['list_name'].iloc[0].replace('-flicker-0','') + "_"
task = galia_flicker_results['taskid'].iloc[0]

galia_flicker_results['_id'].iloc[0] # check the strip

galia_flicker_results[['delete_me','image_1_id','image_2_id']] = galia_flicker_results['_id'].str.split(image_set, expand=True)
galia_flicker_results.drop(columns=["delete_me", "_id"], inplace=True)
galia_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose CDR Desc',
#        'Registration Quality Assessment', 'image 1 opacity', 'image 2 opacity',
#        'fade between images', 'image_1_id', 'image_2_id'],
#       dtype='object')

galia_flicker_results.to_csv(os.path.join(OUT, f"galia_{task}.csv"), index=None)

# ---
stephanie_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose CDR Desc',
#        'Registration Quality Assessment', 'image 1 opacity', 'image 2 opacity',
#        'fade between images'],
#       dtype='object')

stephanie_flicker_results['_id'] = stephanie_flicker_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
stephanie_flicker_results['_id'] = stephanie_flicker_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = stephanie_flicker_results['list_name'].iloc[0].replace('-flicker-0','') + "_"
task = stephanie_flicker_results['taskid'].iloc[0]

stephanie_flicker_results['_id'].iloc[0] # check the strip

stephanie_flicker_results[['delete_me','image_1_id','image_2_id']] = stephanie_flicker_results['_id'].str.split(image_set, expand=True)
stephanie_flicker_results.drop(columns=["delete_me", "_id"], inplace=True)
stephanie_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose CDR Desc',
#        'Registration Quality Assessment', 'image 1 opacity', 'image 2 opacity',
#        'fade between images', 'image_1_id', 'image_2_id'],
#       dtype='object')

stephanie_flicker_results.to_csv(os.path.join(OUT, f"stephanie_{task}.csv"), index=None)

# --- Merge
pd.concat([
steve_flicker_results,
galia_flicker_results,
stephanie_flicker_results,
]).to_csv(os.path.join(OUT, f"all-v2_12_1_23-flicker-0.csv"), index=None)










# Classify Results #
steve_classify_results = c.get_classify_results("mcnamast", "v2_12_1_23-classify-0")

# ---
steve_classify_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Image'], dtype='object')

steve_classify_results['_id'].iloc[0]
steve_classify_results['taskid'].iloc[0]
steve_classify_results['_id'] = steve_classify_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-',''), axis=1)
image_set = steve_classify_results['list_name'].iloc[0].replace('-classify-0','') + "_"
task = steve_classify_results['taskid'].iloc[0]

steve_classify_results['_id'].iloc[0] # check the strip

steve_classify_results[['delete_me','image_id']] = steve_classify_results['_id'].str.split(image_set, expand=True)
steve_classify_results.drop(columns=["delete_me", "_id"], inplace=True)
steve_classify_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Image', 'image_id'], dtype='object')

steve_classify_results.to_csv(os.path.join(OUT, f"steve_{task}.csv"), index=None)

# ---
galia_classify_results = c.get_classify_results("gdeitz", "v2_12_1_23-classify-0")
galia_classify_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Image'], dtype='object')

galia_classify_results['_id'].iloc[0]
galia_classify_results['taskid'].iloc[0]
galia_classify_results['_id'] = galia_classify_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-',''), axis=1)
image_set = galia_classify_results['list_name'].iloc[0].replace('-classify-0','') + "_"
task = galia_classify_results['taskid'].iloc[0]

galia_classify_results['_id'].iloc[0] # check the strip

galia_classify_results[['delete_me','image_id']] = galia_classify_results['_id'].str.split(image_set, expand=True)
galia_classify_results.drop(columns=["delete_me", "_id"], inplace=True)
galia_classify_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Image', 'image_id'], dtype='object')

galia_classify_results.to_csv(os.path.join(OUT, f"galia_{task}.csv"), index=None)


# ---
stephanie_classify_results = c.get_classify_results("swangyu", "v2_12_1_23-classify-0")
stephanie_classify_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Image'], dtype='object')

stephanie_classify_results['_id'].iloc[0]
stephanie_classify_results['taskid'].iloc[0]
stephanie_classify_results['_id'] = stephanie_classify_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-',''), axis=1)
image_set = stephanie_classify_results['list_name'].iloc[0].replace('-classify-0','') + "_"
task = stephanie_classify_results['taskid'].iloc[0]

stephanie_classify_results['_id'].iloc[0] # check the strip

stephanie_classify_results[['delete_me','image_id']] = stephanie_classify_results['_id'].str.split(image_set, expand=True)
stephanie_classify_results.drop(columns=["delete_me", "_id"], inplace=True)
stephanie_classify_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Image', 'image_id'], dtype='object')

stephanie_classify_results.to_csv(os.path.join(OUT, f"stephanie_{task}.csv"), index=None)

# --- Merge
pd.concat([
steve_classify_results,
galia_classify_results,
stephanie_classify_results,
]).to_csv(os.path.join(OUT, f"all-v2_12_1_23-classify-0.csv"), index=None)








# Compare Results #
# ---
steve_compare_results = c.get_compare_results("mcnamast", "v2_12_1_23-compare-0")
steve_compare_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose CDR Desc'], dtype='object')

steve_compare_results['_id'].iloc[0]
steve_compare_results['taskid'].iloc[0]
steve_compare_results['_id'] = steve_compare_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
steve_compare_results['_id'] = steve_compare_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = steve_compare_results['list_name'].iloc[0].replace('-compare-0','') + "_"
task = steve_compare_results['taskid'].iloc[0]

steve_compare_results['_id'].iloc[0] # check the strip

steve_compare_results[['delete_me','image_1_id','image_2_id']] = steve_compare_results['_id'].str.split(image_set, expand=True)
steve_compare_results.drop(columns=["delete_me", "_id"], inplace=True)
steve_compare_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose CDR Desc', 'image_1_id',
#        'image_2_id'],
#       dtype='object')

steve_compare_results.to_csv(os.path.join(OUT, f"steve_{task}.csv"), index=None)

# ---
galia_compare_results = c.get_compare_results("gdeitz", "v2_12_1_23-compare-0")
galia_compare_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose CDR Desc'], dtype='object')

galia_compare_results['_id'].iloc[0]
galia_compare_results['taskid'].iloc[0]
galia_compare_results['_id'] = galia_compare_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
galia_compare_results['_id'] = galia_compare_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = galia_compare_results['list_name'].iloc[0].replace('-compare-0','') + "_"
task = galia_compare_results['taskid'].iloc[0]

galia_compare_results['_id'].iloc[0] # check the strip

galia_compare_results[['delete_me','image_1_id','image_2_id']] = galia_compare_results['_id'].str.split(image_set, expand=True)
galia_compare_results.drop(columns=["delete_me", "_id"], inplace=True)
galia_compare_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose CDR Desc', 'image_1_id',
#        'image_2_id'],
#       dtype='object')

galia_compare_results.to_csv(os.path.join(OUT, f"galia_{task}.csv"), index=None)

# ---
stephanie_compare_results = c.get_compare_results("swangyu", "v2_12_1_23-compare-0")
stephanie_compare_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose CDR Desc'], dtype='object')

stephanie_compare_results['_id'].iloc[0]
stephanie_compare_results['taskid'].iloc[0]
stephanie_compare_results['_id'] = stephanie_compare_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
stephanie_compare_results['_id'] = stephanie_compare_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = stephanie_compare_results['list_name'].iloc[0].replace('-compare-0','') + "_"
task = stephanie_compare_results['taskid'].iloc[0]

stephanie_compare_results['_id'].iloc[0] # check the strip

stephanie_compare_results[['delete_me','image_1_id','image_2_id']] = stephanie_compare_results['_id'].str.split(image_set, expand=True)
stephanie_compare_results.drop(columns=["delete_me", "_id"], inplace=True)
stephanie_compare_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose CDR Desc', 'image_1_id',
#        'image_2_id'],
#       dtype='object')

stephanie_compare_results.to_csv(os.path.join(OUT, f"stephanie_{task}.csv"), index=None)

# --- Merge
pd.concat([
steve_compare_results,
galia_compare_results,
stephanie_compare_results,
]).to_csv(os.path.join(OUT, f"all-v2_12_1_23-compare-0.csv"), index=None)

