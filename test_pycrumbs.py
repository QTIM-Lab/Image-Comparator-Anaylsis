from pathlib import Path
from pycrumbs import tracked


@tracked(literal_directory=Path('/projects/Image-Comparator/preprocessed/RIM-ONE_database_r1/'))
def preprocessed_images_for_app():
    # Do something...
    pass

# Record will be placed at /home/user/proj/my_train_fun_record.json
preprocessed_images_for_app()