import os, pdb
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from matplotlib.colors import ListedColormap

DATA = "/home/bearceb/mnt/QTIM/22-2198/GA_OPTIMEyes/Data"
STATS = "/home/bearceb/mnt/QTIM/22-2198/GA_OPTIMEyes/Stats"

images_and_masks = pd.read_csv(os.path.join(DATA,"image_key.csv"))
images_and_masks.iloc[7]


def load_image(index):
    image_path = images_and_masks.iloc[index]['image']
    mask_path = images_and_masks.iloc[index]['mask']
    image = Image.open(image_path)
    mask = Image.open(mask_path)
    image_np = np.array(image)
    mask_np = np.array(mask)
    # np.unique(mask_np[:,:,0])
    # np.unique(mask_np[:,:,1])
    # np.unique(mask_np[:,:,2])
    # np.unique(mask_np[:,:,3])
    # Extract the grayscale data from the fourth channel
    # pdb.set_trace()
    mask_np_data_r = mask_np[:, :, 0]
    mask_np_data_g = mask_np[:, :, 1]
    mask_np_data_b = mask_np[:, :, 3]
    mask_np_data_a = mask_np[:, :, 3]
    # Convert grayscale data into RGB channels by replicating it across all three channels
    # rgb_channels = np.stack([mask_np_data] * 3, axis=2)
    rgb_channels = np.stack((mask_np_data_r, mask_np_data_g, mask_np_data_b), axis=2)
    # Assign transparency based on a threshold (e.g., 0.5)
    threshold = 0.5
    alpha_channel = np.where(mask_np_data_a > threshold, 50, 0)
    # Stack RGB channels with alpha channel to create RGBA mask
    rgba_mask = np.dstack((rgb_channels, alpha_channel))
    # rgba_mask.shape
    return image_np, rgba_mask

# load_image(7)


# Create a grid of image/mask pairs
num_images = 110
cols = 11
rows = int(num_images / cols)

fig, axes = plt.subplots(rows, cols, figsize=(30, 100))

for i in range(rows):
    for j in range(cols):
        index = i * cols + j
        if index < num_images:
            img, msk = load_image(index)
            # pdb.set_trace()
            # print(f"{img}\n{msk}")
            ax = axes[i, j]
            ax.imshow(img)  # Display the image
            ax.imshow(msk, cmap='jet')  # Overlay the mask
            ax.set_title(f"Image {images_and_masks.iloc[index]['image'][-8:]}")
            # ax.axis('off')


plt.tight_layout()
plt.savefig(os.path.join(STATS, "masks_on_images.png"))
plt.show()