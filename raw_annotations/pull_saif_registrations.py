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
# 03_24_2023 - maybe but updated on 05_2_2023
images = c.get_images(key="saif_registrations")
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

@tracked(literal_directory=Path(OUT))
def write_images_key():
    # images.to_csv(os.path.join(OUT, "opthamology_rim-one.csv"), index=None)
    images.to_csv(os.path.join(OUT, "saif_registrations_images.csv"), index=None)

write_images_key()

# Flicker Results #
Saif_flicker_results = c.get_flicker_results("saif", "saif_reg_approved_chris-flicker-0")
Saif_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose Single Class',
#        'Is the registration adequate?', 'image 1 opacity', 'image 2 opacity',
#        'fade between images'],
#       dtype='object')

Saif_flicker_results['_id'] = Saif_flicker_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
Saif_flicker_results['_id'] = Saif_flicker_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
# image_set = Saif_flicker_results['list_name'].iloc[0].replace('-flicker-0','') + "_"
image_set = 'saif_registrations_' # We manually made a flicker image list from image set saif_registrations but named it without our normal pattern where image lists contain the image set as part of their name.

Saif_flicker_results['_id'].iloc[0]

Saif_flicker_results[['delete_me','image_1_id','image_2_id']] = Saif_flicker_results['_id'].str.split(image_set, expand=True)
Saif_flicker_results.drop(columns=["delete_me", "_id"], inplace=True)
Saif_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose Single Class',
#        'Is the registration adequate?', 'image 1 opacity', 'image 2 opacity',
#        'fade between images', 'image_1_id', 'image_2_id'],
#       dtype='object')

Saif_flicker_results.to_csv(os.path.join(OUT, f"Saif_flicker_results_reg_approved_chris_03_24_2023.csv"), index=None)

