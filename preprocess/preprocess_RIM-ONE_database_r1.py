import os, shutil, pdb
import pandas as pd
from pathlib import Path
from pycrumbs import tracked
from dotenv import load_dotenv
load_dotenv()

DATA_DIR=os.environ["DATA_DIR"]
PROJECTS_DIR=os.environ["PROJECTS_DIR"]

raw_data = os.path.join(DATA_DIR,"RIM-ONE_database_r1")
destination = os.path.join(PROJECTS_DIR,"preprocessed/RIM-ONE_database_r1/")

@tracked(literal_directory=Path(destination))
def identify_desired_images(raw_data: str = raw_data):
    file_ext_desired = '.bmp'
    partial_file_name_to_omit = '-exp'
    folder_classes = ['Normal', 'Early', 'Moderate', 'Deep']
    csv_tuples = []
    # get list of files to move
    for folder in folder_classes:
        files = os.listdir(os.path.join(raw_data, folder))
        files_to_keep = [file for file in files if file.find(file_ext_desired) != -1 and file.find(partial_file_name_to_omit) == -1]
        # move files to destination
        for file in files_to_keep:
            csv_tuples.append((os.path.join(raw_data, folder, file), folder))
            shutil.copy(os.path.join(raw_data, folder, file), os.path.join(destination, file))
    # create image_key.csv
    image_names = [os.path.basename(i[0]) for i in csv_tuples]
    image_paths = [i[0] for i in csv_tuples]
    image_folders = [i[1] for i in csv_tuples]
    images_csv = pd.DataFrame({"image": image_names,
                               "image_path": image_paths,
                               "image_folder": image_folders,
                               })
    # pdb.set_trace()
    # Shuffle
    images_csv = images_csv.sample(frac=1)
    images_csv.to_csv(os.path.join(destination, "image_key.csv"), index=None)

identify_desired_images()