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
PROJECTS_DIR=os.environ["PROJECTS_DIR"]
DNS=os.environ["DNS"]
IMAGES_DB=os.environ["IMAGES_DB"]
DB_PORT=os.environ["DB_PORT"]
DB_ADMIN_USER=os.environ["DB_ADMIN_USER"]
DB_ADMIN_PASS=os.environ["DB_ADMIN_PASS"]
ADMIN_PARTY=True if os.environ["ADMIN_PARTY"] == 'True' else False

c = couch_utils(DNS, DB_PORT, IMAGES_DB, DB_ADMIN_USER, DB_ADMIN_PASS, ADMIN_PARTY)

# Where I will put the csv(s)
OUT = os.path.join(PROJECTS_DIR, "raw_annotations")

# Get Images #
# 01_03_2023 - maybe
# images = c.get_images(key="opthamology_rim-one")
# 03_24_2023 - maybe
images = c.get_images(key="saif_registrations")
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
# Index(['image_path', 'image_folder', 'image_name', 'imageSetName', 'app_image_id'], dtype='object')

@tracked(literal_directory=Path(OUT))
def write_images_key():
    # images.to_csv(os.path.join(OUT, "opthamology_rim-one.csv"), index=None)
    images.to_csv(os.path.join(OUT, "saif_registrations_images.csv"), index=None)

write_images_key()

# Not app id but the IM###.bmp number - very important!!!
images_50 = [4,6,8,11,12,14,16,17,18,20,26,27,28,30,31,34,39,40,45,49,52,56,59,61,63,68,70,71,72,74,78,79,80,81,85,95,98,103,104,114,119,121,129,130,132,145,163,164,165,167]
images['image_name_stripped'] = images['image_name'].str.replace('Im','').str.replace('.bmp','').astype(int)

app_image_ids = list(images[images['image_name_stripped'].isin(images_50)]['app_image_id'])
app_image_ids.sort()

# Classify Results #
# Note: Saif did 158 raw images; others will do 10% more with repeats or 174 rows
# That is why the list name is opthamology_rim-one_ClassifyList versus opthamology_rim-one-10p-repeat_ClassifyList for others
Saif_classify_results = c.get_classification_results("Saif", "opthamology_rim-one_ClassifyList")
Saif_quality_classify_results = c.get_classification_results("Saif_158_redo", "opthamology_rim-one_ClassifyList")

Malik_classify_results = c.get_classification_results("Malik", "opthamology_rim-one-10p-repeat_ClassifyList")
Ittoop_classify_results = c.get_classification_results("Ittoop", "opthamology_rim-one-10p-repeat_ClassifyList")
Lazcano_classify_results = c.get_classification_results("Lazcano", "opthamology_rim-one-10p-repeat_ClassifyList")
Seibold_classify_results = c.get_classification_results("Seibold", "opthamology_rim-one-10p-repeat_ClassifyList")
# We don't have classify results for Alryalat
# Alryalat_classify_results = c.get_classification_results("Alryalat", "opthamology_rim-one-10p-repeat_ClassifyList")

annotator_results = {
    "Saif_classify_results": Saif_classify_results,
    "Saif_quality_classify_results": Saif_quality_classify_results,
    "Malik_classify_results": Malik_classify_results,
    "Ittoop_classify_results": Ittoop_classify_results,
    "Lazcano_classify_results": Lazcano_classify_results,
    "Seibold_classify_results": Seibold_classify_results,
    # "Alryalat_classify_results": Alryalat_classify_results
    }

for df in annotator_results.keys():
    annotator_results[df]['app_image_id'] = annotator_results[df]['image'].apply(os.path.basename)
    annotator_results[df].drop(columns=['_id', '_rev', 'type'], inplace=True)

# join to raw image df
for df in annotator_results.keys():
    # pdb.set_trace()
    annotator_results[df]['app_image_id'] = annotator_results[df]['app_image_id'].astype(int)
    annotator_results[df] = pd.merge(annotator_results[df], images, on="app_image_id")
    annotator_results[df].rename(columns={"image_folder":"diagnosis_original"}, inplace=True)

@tracked(literal_directory=Path(OUT))
def write_classify_results():
    header = ['user', 'image_name', 'diagnosis', 'diagnosis_original', 'justification', 'app_image_id', 'task_idx', 'image_path', 'imageSetName', 'date'] # 'image', 'task', 'task_list_name', -- not included
    for df in annotator_results.keys():
        annotator_results[df][header].to_csv(os.path.join(OUT, f"{df}_11_09_2022.csv"), index=None)

write_classify_results()

# NOTE: Alryalat hasn't finished

# Compare Results #
Malik_compare_results = c.get_compare_results(
    "Malik", "opthamology_rim-one_50_CompareList")
Ittoop_compare_results = c.get_compare_results(
    "Ittoop", "opthamology_rim-one_50_CompareList")
Lazcano_compare_results = c.get_compare_results(
    "Lazcano", "opthamology_rim-one_50_CompareList")
Seibold_compare_results = c.get_compare_results(
    "Seibold", "opthamology_rim-one_50_CompareList")
Alryalat_compare_results = c.get_compare_results(
    "Alryalat", "opthamology_rim-one_50_CompareList")

annotator_results = {
    "Malik_compare_results": Malik_compare_results,
    "Ittoop_compare_results": Ittoop_compare_results,
    "Lazcano_compare_results": Lazcano_compare_results,
    "Seibold_compare_results": Seibold_compare_results,
    "Alryalat_compare_results": Alryalat_compare_results
}

# Malik_compare_results.columns
header = ['user', 'date', 'image0', 'image1', 'winner', 'justification', 'task_list_name', 'task_idx']
for df in annotator_results.keys():
    annotator_results[df].drop(columns=['_id', '_rev', 'type'], inplace=True)
    # annotator_results[df]['app_image_id'] = annotator_results[df]['image'].apply(
    #     os.path.basename)


# join to raw image df
for df in annotator_results.keys():
    annotator_results[df]['image0'] = annotator_results[df]['image0'].astype(int)
    annotator_results[df]['image1'] = annotator_results[df]['image1'].astype(int)
    annotator_results[df] = pd.merge(annotator_results[df], images, left_on="image0", right_on="app_image_id")
    annotator_results[df].drop(columns=['image_path', 'imageSetName', 'app_image_id'], inplace=True)
    annotator_results[df] = pd.merge(annotator_results[df], images, left_on="image1", right_on="app_image_id",suffixes=['_0','_1'])
    annotator_results[df].drop( columns=['image_path', 'imageSetName', 'app_image_id'], inplace=True)
    # pdb.set_trace()
    annotator_results[df].rename(columns={"image_folder_0": "diagnosis_original_0"}, inplace=True)
    annotator_results[df].rename(columns={"image_folder_1": "diagnosis_original_1"}, inplace=True)
    header = ['user', 'date', 'winner', 'image0', 'image1', 'image_name_0', 'image_name_1', 'diagnosis_original_0', 'diagnosis_original_1', 'justification', 'task', 'task_list_name', 'task_idx']
    annotator_results[df] = annotator_results[df][header]

@tracked(literal_directory=Path(OUT))
def write_compare_results():
    for df in annotator_results.keys():
        annotator_results[df][header].to_csv(
            os.path.join(OUT, f"{df}_01_03_2023.csv"), index=None)


# Flicker Results #
Chris_flicker_results = c.get_flicker_results("ClarkQTIM", "saif_registrations-flicker-0")
Chris_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', '_id', 'Choose Single Class',
#        'Is the registration adequate?', 'image 1 opacity', 'image 2 opacity',
#        'fade between images'],
#       dtype='object')
# Chris_flicker_results['app'].iloc[0]
# Chris_flicker_results['taskid'].iloc[0]
# Chris_flicker_results['list_name'].iloc[0]
# Chris_flicker_results['_id'].iloc[0]
Chris_flicker_results['_id'].iloc[0]
Chris_flicker_results['_id'].iloc[1]
Chris_flicker_results['_id'].iloc[2]
Chris_flicker_results['_id'].iloc[3]
Chris_flicker_results['_id'] = Chris_flicker_results.apply(lambda x: x['_id'].replace(x['taskid']+'-result-image1_',''), axis=1)
Chris_flicker_results['_id'] = Chris_flicker_results.apply(lambda x: x['_id'].replace('-image2_',''), axis=1)
image_set = Chris_flicker_results['list_name'].iloc[0].replace('-flicker-0','') + "_"
Chris_flicker_results[['delete_me','image_1_id','image_2_id']] = Chris_flicker_results['_id'].str.split(image_set, expand=True)
Chris_flicker_results.drop(columns=["delete_me", "_id"], inplace=True)
Chris_flicker_results.columns
# Index(['user', 'app', 'taskid', 'list_name', 'Choose Single Class',
#        'Is the registration adequate?', 'image 1 opacity', 'image 2 opacity',
#        'fade between images', 'image_1_id', 'image_2_id'],
#       dtype='object')

Chris_flicker_results.to_csv(os.path.join(OUT, f"Chris_flicker_results_03_24_2023.csv"), index=None)

write_compare_results()