import os, pdb
import SimpleITK as sitk
import cv2 as cv
import numpy as np
from PIL import Image
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


WORKING_DIR = "/sddata/data/RIMR"

### Create Users ###
users = [
  'bbearce', # 1/8
  'bmarks', # 8/8
  'cduic', # 8/8
  'climoli', # 8/8
  'fantaki', # 8/8
  'fsiddig', # 0/8
  'hkhalid', # 8/8
  'idimopoulos', # 8/8 - worried these don't have data
  'jhu', # 8/8
  'kmegid', # 8/8
  'kzhao', # 0/8
  'larguinchona', # 1/8
  'mjhingan', # 8/8
  'mprasad', # 0/8
  'nagi', # 8/8
  'ngim', # 8/8
  'pesfahani', # 8/8
  'rchopra', # 8/8
  'smukherjee', # 8/8
  'tarunachalam', # 8/8
  'tkeenan', # 0/8
]
####################

### Tasks ###
tasks = [{"user":user, "task_id": f"{user}-consensus_grading_ex1-monaiSegmentation-0", "images_path":os.path.join(WORKING_DIR, f"Ex1/{user}-consensus_grading_ex1-monaiSegmentation-0")} for user in users]
tasks[0]
#############

### Get Images and Make Key ###
raw_images = pd.read_csv(os.path.join(WORKING_DIR, "raw_images", "Exercise1", "image_key.csv"))
Ex1_images = raw_images['image_path_orig']
image_key = {f"img_{i}":{"image_name":image, "PIL_Image":None} for i, image in enumerate(Ex1_images)}
print(image_key['img_0'])
print(image_key['img_2'])
###############################



# Folks who finished
for task in tasks:
    # print(task['images_path'])
    images = os.listdir(task['images_path'])
    if len(images) == 8:
        task['finished'] = True
    else:
        task['finished'] = False


fin_tasks = [task for task in tasks if task['finished'] == True]
fin_tasks[0:2]


# Load the original images into key
for img in image_key.keys():
        image_key[img]['PIL_Image'] = np.array( \
            Image.open(os.path.join(WORKING_DIR, \
                                    "raw_images/Exercise1/", \
                                    f"{image_key[img]['image_name']}")
                      )
            )
        image_key[img]['image_path'] = os.path.join(WORKING_DIR, "raw_images/Exercise1/", f"{image_key[img]['image_name']}")
# print(image_key['img_0'])



### Create Segmentations Key ###
segs = {}
for image_generic in image_key.keys():
    segs[f"{image_generic}"] = []
    for task in fin_tasks:
        seg = {
            f"user":task['user'],
            f"image_path": os.path.join(task['images_path'],f"{task['task_id']}-result-consensus_grading_ex1__{image_key[image_generic]['image_name']}")
        }
        segs[f"{image_generic}"].append(seg)
################################


# Read in and Convert to Simple ITK and store in Segmentations Key
for image_generic in image_key.keys():
    for segmentation in segs[image_generic]:
        # Read Image as PIL and cast as ints
        PIL_ints = np.array(Image.open(segmentation['image_path']).convert("L")).astype(np.int32)
        # Threshold to binary mask #
        segmentation['np_binary'] = (PIL_ints > 0).astype(np.int32)
        # Convert to SimpleITK image objects
        segmentation['SITK_Image'] = sitk.GetImageFromArray(segmentation['np_binary'])


# Func to compute STAPLE for all Segmentations
def compute_STAPLE(segs=segs['img_0']):
    # Run STAPLE algorithm
    seg_stack = [seg['SITK_Image'] for seg in segs]
    # STAPLE_seg_sitk = sitk.STAPLE(seg_stack, 1)  # this can be changed
    # Create STAPLE filter
    staple_filter = sitk.STAPLEImageFilter()
    STAPLE_seg_sitk = staple_filter.Execute(seg_stack)
    # pdb.set_trace()
    STAPLE_seg_metrics = {
        "sensitivities": staple_filter.GetSensitivity(),
        "specificities": staple_filter.GetSpecificity()
    }
    # Convert back to numpy array
    STAPLE_seg = sitk.GetArrayFromImage(STAPLE_seg_sitk)
    STAPLE_seg_binary = (STAPLE_seg > 0.5).astype(np.int32)
    # Print statements to inspect the arrays
    # print("STAPLE_seg:", STAPLE_seg.shape, np.unique(STAPLE_seg))
    # print("STAPLE_seg_binary:", STAPLE_seg_binary.shape, np.unique(STAPLE_seg_binary))
    return STAPLE_seg_metrics, STAPLE_seg_binary


# Run Func On All Segmentations
STAPLEs = {}
for image_generic in image_key.keys():
    STAPLE_seg_metrics, STAPLE_seg_binary = compute_STAPLE(segs=segs[image_generic])
    STAPLEs[image_generic] = {
        "staple_mask": STAPLE_seg_binary,
        "metrics": STAPLE_seg_metrics
    }


# Func to Create Plot of Raw Image, Annotator's Segmentations on Image and STAPLE
manually_decided_zooms = {
    "img_0":(1500, 2600, 2000, 1250), # (x_start, x_end, y_start, y_end)
    "img_1":(2000, 2900, 1700, 800), # (x_start, x_end, y_start, y_end)
    "img_2":(400, 1600, 1800, 300), # (x_start, x_end, y_start, y_end)
    "img_3":(170, 600, 600, 160), # (x_start, x_end, y_start, y_end)
    "img_4":(150, 700, 600, 200), # (x_start, x_end, y_start, y_end)
    "img_5":(500, 1500,1400, 700), # (x_start, x_end, y_start, y_end)
    "img_6":(1500, 3000, 2000, 900), # (x_start, x_end, y_start, y_end)
    "img_7":(1300, 2200,  2000, 1200), # (x_start, x_end, y_start, y_end)
}

def generate_all_image_views(image_generic='img_0'):
    # visualize the staple result
    fig, axes = plt.subplots(2, 2 + len(fin_tasks), figsize=(40, 6))
    # pdb.set_trace()
    for row_index, row_of_axes in enumerate(axes):
        # Display the original image
        if row_index == 0:
            row_of_axes[0].set_title(f"{image_key[image_generic]['image_name'][-12:]}")
            row_of_axes[0].imshow(image_key[image_generic]['PIL_Image'])
        else:
            row_of_axes[0].set_xlim(manually_decided_zooms[image_generic][0], manually_decided_zooms[image_generic][1])
            row_of_axes[0].set_ylim(manually_decided_zooms[image_generic][2], manually_decided_zooms[image_generic][3])
            row_of_axes[0].set_title(f"{image_key[image_generic]['image_name'][-12:]}")
            row_of_axes[0].imshow(image_key[image_generic]['PIL_Image'])
        for i, axis in enumerate(row_of_axes[1:-1]):
            print(f"making axis {i}")
            # Display segmentations from each rater
            axis.set_title(f"ann {i}")
            # axis.set_title(f"{segs[image_generic][i]['user']}")
            if row_index == 0:
                axis.imshow(image_key[image_generic]['PIL_Image'])
                # pdb.set_trace()
                red_mask = np.ma.masked_where(segs[image_generic][i]['np_binary'] == 0, segs[image_generic][i]['np_binary'])
                axis.imshow(segs[image_generic][i]['np_binary'], cmap="Reds", interpolation="none", alpha=0.6)
            else:
                red_staple = np.ma.masked_where(STAPLEs[image_generic]["staple_mask"] == 0, STAPLEs[image_generic]["staple_mask"])
                axis.imshow(STAPLEs[image_generic]["staple_mask"], cmap="Greens", interpolation="none", alpha=1)
                yellow_mask = np.ma.masked_where(segs[image_generic][i]['np_binary'] == 0, segs[image_generic][i]['np_binary'])
                axis.imshow(segs[image_generic][i]['np_binary'] , cmap="Reds", interpolation="none", alpha=0.5)
                axis.set_xlim(manually_decided_zooms[image_generic][0], manually_decided_zooms[image_generic][1])
                axis.set_ylim(manually_decided_zooms[image_generic][2], manually_decided_zooms[image_generic][3])
        # Display STAPLE result
        row_of_axes[-1].set_title("STAPLE")
        if row_index == 0:
            row_of_axes[-1].imshow(image_key[image_generic]['PIL_Image'])
            row_of_axes[-1].imshow(STAPLEs[image_generic]["staple_mask"], cmap="Greens", interpolation="none", alpha=0.6)
        else:            
            row_of_axes[-1].set_xlim(manually_decided_zooms[image_generic][0], manually_decided_zooms[image_generic][1])
            row_of_axes[-1].set_ylim(manually_decided_zooms[image_generic][2], manually_decided_zooms[image_generic][3])
            row_of_axes[-1].imshow(image_key[image_generic]['PIL_Image'])
            row_of_axes[-1].imshow(STAPLEs[image_generic]["staple_mask"], cmap="Greens", interpolation="none", alpha=0.6)
        # fig.set_size_inches(16, 12)
    plt.savefig(os.path.join(WORKING_DIR, "Stats", f"all_image_views_{image_generic}.png"), dpi = 300)
    # plt.show()
    # pdb.set_trace()




# Run Func to make plots
for image_generic in image_key.keys():
    generate_all_image_views(image_generic=image_generic)



# Create Contours Key in Segs var
for image_generic in image_key.keys():
    # image_generic = 'img_0'
    for segmentation in segs[image_generic]:
        # segmentation = segs[image_generic][0]
        im = cv.imread(segmentation['image_path'])
        imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 50, 255, 0) # Seems we have 70
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # pdb.set_trace()
        segmentation['contours'] = contours


# Func to Create Plot of Raw Image, Annotator's Segmentation Contours



# Assuming you have a list of raw images and a list of sets of contours
raw_images = [image_key[ik]['PIL_Image'] for ik in image_key.keys()]  # List of raw images
# contours_list = [[segs[ik][j]['contours'] for j in range(len(segs[ik]))] for ik in image_key.keys()] # List of sets of contours
contours_list = [{segs[ik][j]['user']:segs[ik][j]['contours'] for j in range(len(segs[ik]))} for ik in image_key.keys()] # List of sets of contours
# >>> contours_list[0].keys()
# dict_keys(['bmarks', 'cduic', 'climoli', 'fantaki', 'hkhalid', 'idimopoulos', 'jhu', 'ngim', 'pesfahani', 'smukherjee'])



# Loop through each raw image and its corresponding set of contours
for raw_image, img_contours, image_generic in zip(raw_images, contours_list, image_key.keys()):
    # Dummy Sample
    # raw_image, img_contours, image_generic = list(zip(raw_images, contours_list, image_key.keys()))[0]
    # Set up subplots with 1 row and 2 columns
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
    def force_RGB(height, width, raw_image, channels):
        # pdb.set_trace()
        # Create a three-channel RGB image by duplicating the grayscale values
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
        rgb_image[:,:,0] = raw_image if channels == 1 else raw_image[:,:,0]   # Red channel
        rgb_image[:,:,1] = raw_image if channels == 1 else raw_image[:,:,1]   # Green channel
        rgb_image[:,:,2] = raw_image if channels == 1 else raw_image[:,:,2]   # Blue channel
        return rgb_image
    if len(raw_image.shape) > 2:
        height, width, _ = raw_image.shape
        raw_image = force_RGB(height, width, raw_image, channels=_)
    elif len(raw_image.shape) == 2:
        height, width = raw_image.shape
        raw_image = force_RGB(height, width, raw_image, channels=1)
    else:
        raise Exception("unhandled shape")
    # if image_generic == 'img_4':
    #     pdb.set_trace()
    # # Display raw image in the left plot
    # axes[0].imshow(raw_image)
    # axes[0].set_title('Raw Image')
    # Create a blank image to draw img_contours on
    # contour_image = np.zeros((height, width, 3), dtype=np.uint8) # Blank
    contour_image = raw_image.copy() # raw_image background
    # Draw each set of img_contours with a different color
    # Initialize an empty list to hold legend patches
    contours_legend_patches = []
    legend_colors = []
    # for idx, annotator_contours in enumerate(img_contours):
    for i, annotator in enumerate(img_contours.keys()):
    # for i, annotator in enumerate(img_contours.keys()[0]):
        # i, annotator = 0, 'bmarks'
        annotator_contours = img_contours[annotator]
        color = tuple(np.random.randint(0, 255, 3).tolist())  # Generate a random color
        # Draw the contours on a separate temporary image
        temp_image = np.zeros_like(contour_image)
        # drawn_contour_image = cv.drawContours(temp_image, annotator_contours, -1, color, thickness=14)
        cv.drawContours(contour_image, annotator_contours, -1, color, thickness=int(14*(width/4000)))
        # Blend the temporary image with the original
        # alpha = 0.098  # Transparency factor
        # Update contour_image by blending it with temp_image
        # cv.addWeighted(temp_image, alpha, contour_image, 1-alpha, 0, contour_image)
        # Create a patch for the legend with the random color and a label
        n_color = tuple((v / 255.0 for v in color)) # normalize for mpatches.Patch
        contours_legend_patch = mpatches.Patch(color=n_color, label=f'Ann {i}')
        legend_colors.append(n_color)
        contours_legend_patches.append(contours_legend_patch)
    # Display the contours in the right plot
    axes[0].imshow(contour_image)
    axes[0].set_title('Contours')
    # Add the legend to the right subplot
    ## Add space for the legend
    plt.subplots_adjust(wspace=0)
    # Add the legend in a separate subplot (optional)
    # ax_legend = axes[0].inset_axes([1.1, 0, 0.2, 1])  # Adjust position and size as needed
    # ax_legend.legend(handles=contours_legend_patches, loc='center', title='Legend')
    # ax_legend.axis('off')
    # axes[0].legend(handles=contours_legend_patches, loc='upper left')
    # STAPLE plot
    axes[1].set_title('STAPLE')
    axes[1].imshow(raw_image)
    axes[1].imshow(STAPLEs[image_generic]['staple_mask'], cmap="Reds", interpolation="none", alpha=0.5)
    # Add the legend in a separate subplot (optional)
    STAPLE_legend_patches = [mpatches.Patch(color=legend_colors[i], label=f"Ann {i} Sens: {round(STAPLEs[image_generic]['metrics']['sensitivities'][i], 3)} Spec: {round(STAPLEs[image_generic]['metrics']['specificities'][i], 3)}") for i, annotator in enumerate(img_contours.keys())]
    ax_legend_STAPLE = axes[1].inset_axes([-.35 if width > 3000 else -.55, 0.5, 0, 0])  # Adjust position and size as needed
    ax_legend_STAPLE.legend(handles=STAPLE_legend_patches, loc='center', title='Legend')
    ax_legend_STAPLE.axis('off')
    # Adjust layout and display the plots
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(WORKING_DIR, "Stats", f"all_contours_views_{image_generic}.png"), dpi = 300)
    # pdb.set_trace()



### VARS ###
users # []

tasks # [{},{}]
fin_tasks # [{},{}]

raw_images # df
image_key # dict - dict_keys(['img_0', 'img_1', 'img_2', 'img_3', 'img_4', 'img_5', 'img_6', 'img_7'])

segs # dict - dict_keys(['img_0', 'img_1', 'img_2', 'img_3', 'img_4', 'img_5', 'img_6', 'img_7'])

images # Source Image [np.array]


contours
### VARS ###