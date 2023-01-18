import os, pdb, pandas as pd, numpy as np, math
from pull_from_couchdb.couch import couch_utils

pd.set_option('display.max_colwidth', 100) # Column width in px
pd.set_option('display.max_rows', 100)

DNS='image-comparator.eastus.cloudapp.azure.com'
IMAGES_DB='image_comparator'

DB_PORT='5991'
DB_ADMIN_USER='admin'
DB_ADMIN_PASS='optha_pa$$w0rd_BB'

ADMIN_PARTY=False

c = couch_utils(DNS, DB_PORT, IMAGES_DB, DB_ADMIN_USER, DB_ADMIN_PASS, ADMIN_PARTY)

# Where I will put the csv(s)
OUT = "couchdb_results/Opthamology/RIM-ONE"

# Get Images #
images = c.get_images(key="opthamology_rim-one")
images.columns
# Index(['_id', '_rev', 'image_path', 'image_folder', 'origin', 'id', 'type', 'imageSetName', 'timeAdded'], dtype='object')

images['image_path']
images['app_image_id'] = images['_id']
images['app_image_id'] = images['app_image_id'].astype(int)
images.rename(columns={'origin':'image_name'}, inplace=True)
images.drop(columns=['_id', '_rev', 'type', 'timeAdded', 'id'], inplace=True)
images.columns
# Index(['image_path', 'image_folder', 'image_name', 'imageSetName', 'app_image_id'], dtype='object')
images.to_csv(os.path.join(OUT, "images.csv"), index=None)

# Not app id but the IM###.bmp number - very important!!!
images_50 = [4,6,8,11,12,14,16,17,18,20,26,27,28,30,31,34,39,40,45,49,52,56,59,61,63,68,70,71,72,74,78,79,80,81,85,95,98,103,104,114,119,121,129,130,132,145,163,164,165,167]
images['image_name_stripped'] = images['image_name'].str.replace('Im','').str.replace('.bmp','').astype(int)

app_image_ids = list(images[images['image_name_stripped'].isin(images_50)]['app_image_id'])
app_image_ids.sort()

# Classify Results #
# Note: Saif did 158 raw images; others will do 10% more with repeats or 174 rows
# That is why the list name is opthamology_rim-one_ClassifyList versus opthamology_rim-one-10p-repeat_ClassifyList for others
Saif_classify_results = c.get_classification_results("Saif", "opthamology_rim-one_ClassifyList")
Saif_quality_classify_results = c.get_classification_results(
    "Saif_158_redo", "opthamology_rim-one_ClassifyList")


Malik_classify_results = c.get_classification_results("Malik", "opthamology_rim-one-10p-repeat_ClassifyList")
Ittoop_classify_results = c.get_classification_results("Ittoop", "opthamology_rim-one-10p-repeat_ClassifyList")
Lazcano_classify_results = c.get_classification_results("Lazcano", "opthamology_rim-one-10p-repeat_ClassifyList")
Seibold_classify_results = c.get_classification_results("Seibold", "opthamology_rim-one-10p-repeat_ClassifyList")
Alryalat_classify_results = c.get_classification_results("Alryalat", "opthamology_rim-one-10p-repeat_ClassifyList")

annotator_results = {
    # "Saif_classify_results": Saif_classify_results,
    "Saif_quality_classify_results": Saif_quality_classify_results,
    # "Malik_classify_results": Malik_classify_results,
    # "Ittoop_classify_results": Ittoop_classify_results,
    # "Lazcano_classify_results": Lazcano_classify_results,
    # "Seibold_classify_results": Seibold_classify_results,
    # "Alryalat_classify_results": Alryalat_classify_results
    }
for df in annotator_results.keys():
    annotator_results[df]['app_image_id'] = annotator_results[df]['image'].apply(os.path.basename)
    annotator_results[df].drop(columns=['_id', '_rev', 'type'], inplace=True)

annotator_results

# join to raw image df
for df in annotator_results.keys():
    annotator_results[df] = pd.merge(annotator_results[df], images, on="app_image_id")
    annotator_results[df]['app_image_id'] = annotator_results[df]['app_image_id'].astype(int)
    annotator_results[df].rename(columns={"image_folder":"diagnosis_original"}, inplace=True)
    # pdb.set_trace()

annotator_results['Saif_quality_classify_results'].columns
# Index(['user', 'date', 'image', 'diagnosis', 'task', 'task_list_name', 'task_idx', 'app_image_id', 'image_path', 'diagnosis_original', 'image_name', 'imageSetName'], dtype='object')

header = ['user', 'image_name', 'diagnosis', 'diagnosis_original', 'justification', 'app_image_id', 'task_idx', 'image_path', 'imageSetName', 'date'] # 'image', 'task', 'task_list_name', -- not included
for df in annotator_results.keys():
    annotator_results[df][header].to_csv(os.path.join(OUT, f"{df}_11_09_2022.csv"), index=None)

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
annotator_results.keys()

# Malik_compare_results.columns
header = ['user', 'date', 'image0', 'image1', 'winner', 'justification', 'task_list_name', 'task_idx']
Malik_compare_results[header]['image0']

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
    annotator_results[df].columns
    annotator_results[df].rename(columns={"image_folder_0": "diagnosis_original_0"}, inplace=True)
    annotator_results[df].rename(columns={"image_folder_1": "diagnosis_original_1"}, inplace=True)
    header = ['user', 'date', 'winner', 'image0', 'image1', 'image_name_0', 'image_name_1', 'diagnosis_original_0', 'diagnosis_original_1', 'justification', 'task', 'task_list_name', 'task_idx']
    annotator_results[df] = annotator_results[df][header]

for df in annotator_results.keys():
    annotator_results[df][header].to_csv(
        os.path.join(OUT, "compare_results_01_03_2023", f"{df}_01_03_2023.csv"), index=None)

# annotator_results['Malik_compare_results'].columns
# annotator_results[' '].columns

