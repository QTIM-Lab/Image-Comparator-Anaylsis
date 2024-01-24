import os, shutil, pdb
import pandas as pd

pd.set_option('display.max_colwidth', 1000) # Column width in px

from pathlib import Path
# from pycrumbs import tracked
from dotenv import load_dotenv
load_dotenv()

INPUT=os.environ["PROJECT_INPUT_DATA_DIR"]
OUTPUT=os.environ["PROJECT_DIR"]

csv_path = os.path.join(INPUT, "csvs", "rim_one_special_segformer_v3_segmentations.csv")

csv = pd.read_csv(csv_path)
csv.drop("Unnamed: 0", inplace=True, axis=1)
csv.columns # Index(['Image', 'Segmentation', 'Overlay', 'Detailed'], dtype='object')
csv.head()

# We want Image, Segmentation and Overlay

# @tracked(literal_directory=Path(OUTPUT))
def identify_desired_images(csv, copy_images=True):
    images = list(csv['Image'])
    segmentations = csv['Segmentation']
    overlays = csv['Overlay']
    # get list of files to move
    app_img_paths = []
    app_seg_paths = []
    app_overlay_paths = []
    for img, seg, overlay in zip(images, segmentations, overlays):
        # move files to OUTPUT
        # First copy original
        img_path = os.path.dirname(img.replace(INPUT+"/", ""))
        img_name = os.path.basename(img.replace(INPUT+"/", ""))
        app_img_paths.append((img_path, img_name))
        if not os.path.exists(os.path.join(OUTPUT, img_path)):
            os.makedirs(os.path.join(OUTPUT, img_path))
        
        seg_path = os.path.dirname(seg.replace(INPUT+"/", ""))
        seg_name = os.path.basename(seg.replace(INPUT+"/", ""))
        app_seg_paths.append((seg_path, seg_name))
        if not os.path.exists(os.path.join(OUTPUT, seg_path)):
            os.makedirs(os.path.join(OUTPUT, seg_path))
        
        overlay_path = os.path.dirname(overlay.replace(INPUT+"/", ""))
        overlay_name = os.path.basename(overlay.replace(INPUT+"/", ""))
        app_overlay_paths.append((overlay_path, overlay_name))
        if not os.path.exists(os.path.join(OUTPUT, overlay_path)):
            os.makedirs(os.path.join(OUTPUT, overlay_path))
            
        if copy_images == True:
            shutil.copy(os.path.join(INPUT, os.path.join(img_path, img_name)), os.path.join(OUTPUT, img_path, img_name))
            shutil.copy(os.path.join(INPUT, os.path.join(seg_path, seg_name)), os.path.join(OUTPUT, seg_path, seg_name))
            shutil.copy(os.path.join(INPUT, os.path.join(overlay_path, overlay_name)), os.path.join(OUTPUT, overlay_path, overlay_name))
    # create image_key.csv
    
    pdb.set_trace()
    header = ["image", "image_path_orig", "relative_path", "image_type"]
    image_names = [i[1] for i in app_img_paths] + [i[1] for i in app_overlay_paths]
    relative_path = [i[0] for i in app_img_paths] + [i[0] for i in app_overlay_paths]
    image_path_orig = list(images) + list(overlays)
    image_type = ["first" for i in images] + ["second" for i in overlays]
    
    
    images_csv = {"image":image_names, "image_path_orig": image_path_orig, "relative_path": relative_path, "image_type": image_type}
    images_csv = pd.DataFrame(images_csv)
    images_csv = images_csv.sort_values("image")
    
    # Shuffle
    # images_csv = images_csv.sample(frac=1)
    images_csv.to_csv(os.path.join(OUTPUT, "image_key.csv"), index=None)

identify_desired_images(csv, copy_images=True)