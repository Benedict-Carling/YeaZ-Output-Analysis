import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation

CELLFOLDER = "april5"
CELLPATH = "data/" + CELLFOLDER + "/cells-ratio.pkl"


df = pd.read_pickle(CELLPATH)

## Gaussian Blur
## Find largest pixel's
## Erode and Expand
## That is the best guess of the nucleus
## Then find the ratio


def flatten(lst):
    """
    Flattens a nested list into a single list.
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def grayscale_to_binary(image, threshold):
    """
    Converts a grayscale image to a binary image based on a threshold value.
    """
    binary = np.where(image > threshold, 1, 0)
    return binary


def apply_gaussian_blur(image, sigma):
    """
    Applies a Gaussian blur to a grayscale image.
    """
    blurred_image = gaussian_filter(image, sigma=sigma)
    return blurred_image


def erode_then_dilate(image, kernel_size):
    """
    Applies erosion and dilation to a grayscale image using a given kernel size.
    """
    kernel = np.ones((kernel_size, kernel_size), dtype=bool)
    eroded = binary_erosion(image, structure=kernel)
    dilated = binary_dilation(eroded, structure=kernel)
    return dilated


def get_cell_nucleus(bfp_channel):
    blurred_image = apply_gaussian_blur(bfp_channel, sigma=1)
    withoutzeros = blurred_image[blurred_image != 0]
    p = np.percentile(withoutzeros, 85)
    binary_image = grayscale_to_binary(blurred_image, p)
    result_image = erode_then_dilate(binary_image, kernel_size=3)
    return result_image


def mean_pixel_value(image, mask):
    """
    Finds the mean pixel value of a grayscale image within a binary mask.
    """
    # Apply the mask to the image
    # Find the mean pixel value of the masked image
    multiplied_mask = np.multiply(image, mask)
    mean = multiplied_mask[multiplied_mask != 0]
    return np.mean(mean)


def invert_binary_image(image):
    """
    Inverts a binary segmentation image.
    """
    inverted_image = np.logical_not(image)
    return inverted_image


def nuclear_cytosolic_ratio(gfp_channel, bfp_channel):
    nucleus_mask = get_cell_nucleus(bfp_channel)
    nuclear_score = mean_pixel_value(gfp_channel, nucleus_mask)
    cytosolic_score = mean_pixel_value(gfp_channel, invert_binary_image(nucleus_mask))
    return nuclear_score / cytosolic_score


df = df.set_index("cellId")
df = df[df["score1"].isna()]
print(df)
item = df.loc[2]

print(item)


# # nuc = get_cell_nucleus(item["blueCell1"])
# # score = nuclear_cytosolic_ratio(item["greenCell1"],nuc)
# # print(score)

# plt.imshow(item["blueCell1"], interpolation='nearest')
# plt.show()

# nuc = get_cell_nucleus(item["blueCell1"])

# nuclear_score = mean_pixel_value(item["greenCell1"],nuc)
# cytosolic_score = mean_pixel_value(item["greenCell1"],invert_binary_image(nuc))
# ratio = nuclear_cytosolic_ratio(item["greenCell1"],item["blueCell1"])
# print(nuclear_score)
# print(cytosolic_score)

# print(nuclear_score / cytosolic_score)
# print(ratio)
# plt.imshow(nuc, interpolation='nearest')
# plt.show()

# gray_image = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])

# # Create a binary mask
# mask = np.array([[1, 1, 0], [0, 1, 0], [0, 1, 1]])

# # Find the mean pixel value of the grayscale image within the mask
# mean_value = mean_pixel_value(gray_image, mask)

# # Print the result
# print(mean_value)
