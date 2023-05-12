import os, shutil, pdb
import pandas as pd
from pathlib import Path
# from pycrumbs import tracked
from dotenv import load_dotenv
load_dotenv()

INPUT=os.environ["DATA_DIR"]
OUTPUT=os.environ["PROJECT_DIR"]

# @tracked(literal_directory=Path(OUTPUT))
def identify_desired_images(INPUT: str = INPUT):
    file_ext_desired = '.bmp'
    partial_file_name_to_omit = '-exp'
    folder_classes = ['Normal', 'Early', 'Moderate', 'Deep']
    csv_tuples = []
    # get list of files to move
    for folder in folder_classes:
        files = os.listdir(os.path.join(INPUT, folder))
        files_to_keep = [file for file in files if file.find(file_ext_desired) != -1 and file.find(partial_file_name_to_omit) == -1]
        # move files to OUTPUT
        for file in files_to_keep:
            csv_tuples.append((os.path.join(INPUT, folder, file), folder))
            if not os.path.exists(os.path.join(OUTPUT, folder)):
                os.mkdir(os.path.join(OUTPUT, folder))
            shutil.copy(os.path.join(INPUT, folder, file), os.path.join(OUTPUT, folder, file))
    # create image_key.csv
    image_names = [os.path.basename(i[0]) for i in csv_tuples]
    orig_image_paths = [i[0] for i in csv_tuples]
    image_folders = [i[1] for i in csv_tuples]
    image_relative_paths = [i.replace(INPUT+"/", "") for i in orig_image_paths]
    images_csv = pd.DataFrame({"image": image_names,
                               "orig_image_path": orig_image_paths,
                               "relative_path": image_relative_paths,
                               "image_classification": image_folders,
                               })
    # pdb.set_trace()
    # Shuffle
    # images_csv = images_csv.sample(frac=1)
    images_csv.to_csv(os.path.join(OUTPUT, "image_key.csv"), index=None)

identify_desired_images()