import cv2
import numpy as np

from helper_analysis_path import CELLPATH
from helper_analysis_path import CELLDIRECTORY
from helper_analysis_path import FILENAME


def gray_to_neon_green(gray_path, output_path):
    # Load grayscale image
    gray = cv2.imread(gray_path, cv2.IMREAD_GRAYSCALE)

    # Create an RGB version of the grayscale image for colorization
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    # Define the neon green color for the image
    color = (0, 255, 0)

    # Threshold the grayscale image to create a binary mask of non-black pixels
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Apply the mask to the RGB image to change only the non-black pixels to neon green
    gray_rgb[mask != 0] = color

    # Save the output image
    cv2.imwrite(output_path, gray_rgb)


def overlay_images(lower_path, upper_path, output_path):
    # Load lower and upper images
    lower_gray = cv2.imread(lower_path, cv2.IMREAD_GRAYSCALE)
    lower = cv2.cvtColor(lower_gray, cv2.COLOR_GRAY2RGB)
    upper = cv2.imread(upper_path, cv2.IMREAD_COLOR)

    # Create a binary mask of non-black pixels in the upper image
    _, mask = cv2.threshold(
        cv2.cvtColor(upper, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY
    )

    # Invert the mask so that black pixels become white and vice versa
    mask_inv = cv2.bitwise_not(mask)

    # Create a copy of the lower image to use as the output
    output = lower.copy()

    # Set the pixels in the output to be the corresponding pixels from the upper image
    output[np.where(mask == 255)] = upper[np.where(mask == 255)]

    # Set the pixels in the output to be the corresponding pixels from the lower image where the upper image is black
    output[np.where(mask_inv == 255)] = lower[np.where(mask_inv == 255)]

    # Save the output image
    cv2.imwrite(output_path, output)


def overlay_images_2(lower_path, upper_path1, upper_path2, output_path):
    # Load lower and upper images
    lower_gray = cv2.imread(lower_path, cv2.IMREAD_GRAYSCALE)
    lower = cv2.cvtColor(lower_gray, cv2.COLOR_GRAY2RGB)
    upper1 = cv2.imread(upper_path1, cv2.IMREAD_COLOR)
    upper2 = cv2.imread(upper_path2, cv2.IMREAD_COLOR)

    # Create binary masks of non-black pixels in the upper images
    _, mask1 = cv2.threshold(
        cv2.cvtColor(upper1, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY
    )
    _, mask2 = cv2.threshold(
        cv2.cvtColor(upper2, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY
    )

    # Combine the masks to create a single mask
    combined_mask = cv2.bitwise_or(mask1, mask2)

    # Invert the mask so that black pixels become white and vice versa
    mask_inv = cv2.bitwise_not(combined_mask)

    # Create a copy of the lower image to use as the output
    output = lower.copy()

    # Set the pixels in the output to be the corresponding pixels from the first upper image
    output[np.where(mask1 == 255)] = upper1[np.where(mask1 == 255)]

    # Set the pixels in the output to be the corresponding pixels from the second upper image where the first upper image is black
    output[np.where(mask1 == 0) and np.where(mask2 == 255)] = upper2[
        np.where(mask1 == 0) and np.where(mask2 == 255)
    ]

    # Set the pixels in the output to be the corresponding pixels from the lower image where the upper images are black
    output[np.where(mask_inv == 255)] = lower[np.where(mask_inv == 255)]

    # Save the output image
    cv2.imwrite(output_path, output)


for i in range(1, 384):
    try:
        outdir = CELLDIRECTORY + "overlap"
        indir = CELLDIRECTORY + "raw_images"
        maskdir = CELLDIRECTORY + "subpop_masks"
        outline1 = "{}/{}_blue_mask.png".format(maskdir, i)
        outline2 = "{}/{}_red_mask.png".format(maskdir, i)
        overlay_images_2(
            "{}/{}_Mono.png".format(indir, i),
            outline1,
            outline2,
            "{}/{}_Mono.png".format(outdir, i),
        )
        overlay_images_2(
            "{}/{}_Green.png".format(indir, i),
            outline1,
            outline2,
            "{}/{}_Green.png".format(outdir, i),
        )
    except:
        print("Unable to process", i)
