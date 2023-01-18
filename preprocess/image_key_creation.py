import os, pdb, pandas as pd, numpy as np, shutil, random

pd.set_option('display.max_columns', 100) # How many to show
pd.set_option('display.min_rows', 25) # How many to show
pd.set_option('display.max_rows', 50) # How many to show
pd.set_option('display.width', 1000) # How far across the screen
pd.set_option('display.max_colwidth', 1) # Column width in px
pd.set_option('display.max_colwidth', 100) # Column width in px
pd.set_option('expand_frame_repr', True) # allows for the representation of dataframes to stretch across pages, wrapped over the full column vs row-wise

raw_images_path = "raw_images/Opthamology/RIM-ONE_database_r1"
image_comparator_set_path = os.path.join(raw_images_path, "Image_Comparator_Set")

deep_files = os.listdir(os.path.join(raw_images_path, "Deep"))
early_files = os.listdir(os.path.join(raw_images_path, "Early"))
moderate_files = os.listdir(os.path.join(raw_images_path, "Moderate"))
normal_files = os.listdir(os.path.join(raw_images_path, "Normal"))

# Jayashree wants
deep_files = [i for i in deep_files if i.find("exp") == -1 and i.find(".csv") == -1]
early_files = [i for i in early_files if i.find("exp") == -1 and i.find(".csv") == -1]
moderate_files = [i for i in moderate_files if i.find("exp") == -1 and i.find(".csv") == -1]
normal_files = [i for i in normal_files if i.find("exp") == -1 and i.find(".csv") == -1]

len(deep_files) # 14
len(early_files) # 12
len(moderate_files) # 14
len(normal_files) # 118
# 118+14+12+14 # 158

# Create csv mapping file
D = [(os.path.join(raw_images_path, "Deep", i), "Deep") for i in deep_files]
E = [(os.path.join(raw_images_path, "Early", i), "Early") for i in early_files]
M = [(os.path.join(raw_images_path, "Moderate", i), "Moderate") for i in moderate_files]
N = [(os.path.join(raw_images_path, "Normal", i), "Normal") for i in normal_files]

# Build csv
images = D+E+M+N
image_paths = [i[0] for i in images]
image_names = [os.path.basename(i) for i in image_paths]
image_folders = [i[1] for i in images]

images_csv = pd.DataFrame({"image": image_names,
                           "image_path": image_paths,
                           "image_folder": image_folders,
                           })

# Shuffle
images_csv = images_csv.sample(frac=1)

# Copy images we want to Image_Comparator_Set folder
def copy_images():
    for image in images_csv['image']:
        # pdb.set_trace()
        shutil.copyfile(src=os.path.join(image), dst=os.path.join(image_comparator_set_path, os.path.basename(image)))
    # len(os.listdir(image_comparator_set_path))

# copy_images()

images_csv.to_csv(os.path.join(image_comparator_set_path, "image_key.csv"), index=None)

# Question for Jayashree
# * 4 level classification - radio buttons (single-choice) or checkboxes (multi-choice)