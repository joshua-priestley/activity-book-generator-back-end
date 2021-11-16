from flask import Blueprint, request
from PIL import Image
import random
import math


def image_shuffler(original_img_path, num_tiles):
    # Opens image from given file path
    try:
        original_img = Image.open(original_img_path)
    except IOError:
        print("No image found at filepath")
        original_img = Image.open('christmas.jpg')
        pass

    width, height = original_img.size

    num_w_tiles = 1
    num_h_tiles = 1

    # If number of tiles is greater than 1, splits into tiles and concatenates shuffles tiles into another image
    if num_tiles > 1:
        # Calculates the optimum splits for each side of the puzzle to keep tiles most square like
        (num_w_tiles, num_h_tiles) = calc_num_splits_on_each_side(width, height, num_tiles)

        # Splits images into tiles
        tile_list, area_list = split_into_tiles(width, height, num_w_tiles, num_h_tiles, original_img)

        # Shuffles tiles and combines them into one image
        shuffled_image = concatenate_tiles(tile_list, width, height, area_list)

    # If number of tiles is 1 or less, then return original image
    else:
        shuffled_image = original_img

    shuffled_image_path = original_img_path[0:-4] + "_shuffled.jpg"

    # Save shuffled image
    shuffled_image.save(shuffled_image_path)

    return shuffled_image_path, num_w_tiles, num_h_tiles


def calc_num_splits_on_each_side(width, height, num_tiles):

    # Get factor pairs of num_tiles
    factors = []
    for whole_number in range(1, int(math.sqrt(num_tiles)) + 1):
        if num_tiles % whole_number == 0:
            factors.append((whole_number, num_tiles // whole_number))

    # For each factor pair, divides the longest side by the largest factor, and the shortest side by the smallest
    # factor, calculates the difference between width and height splits and picks the best number of splits for each
    # side to ensure tile width and height are most square-like
    smallest_diff = max(width, height)
    w_num_tiles = 0
    h_num_tiles = 0
    for i, factor_pair in enumerate(factors):
        diff = (max(width, height) / max(factor_pair) - min(width, height) / min(factor_pair))
        diff = abs(diff)
        if diff < smallest_diff:
            smallest_diff = diff
            if width >= height:
                w_num_tiles = max(factor_pair)
                h_num_tiles = min(factor_pair)
            else:
                w_num_tiles = min(factor_pair)
                h_num_tiles = max(factor_pair)

    return w_num_tiles, h_num_tiles


def split_into_tiles(width, height, num_w_t, num_h_t, original_img):
    area_list = []
    tile_list = []

    # Calculates width and height split points
    width_splits = [i * width / num_w_t for i in range(0, num_w_t + 1)]
    height_splits = [i * height / num_h_t for i in range(0, num_h_t + 1)]

    # Creates a list of areas for the tiles using the width and height split points
    for i in range(0, num_w_t):
        for j in range(0, num_h_t):
            area_list.append((width_splits[i], height_splits[j], width_splits[i + 1], height_splits[j + 1]))

    # Crops the image for each area and creates a list of tiles
    for i, area in enumerate(area_list):
        tile_list.append(original_img.crop(area))

    return tile_list, area_list


def concatenate_tiles(tile_list, width, height, area_list):
    # Create a new image with original size
    shuffled_image = Image.new('RGB', (width, height))

    # Shuffle the tile list making sure no tile is in same position as previously
    randomized_list = tile_list[:]
    shuffled = False
    while not shuffled:
        random.shuffle(randomized_list)
        for a, b in zip(tile_list, randomized_list):
            if a == b:
                break
        else:
            shuffled = True
    tile_list = randomized_list

    # Paste in shuffled tiles in the new image
    for i, area in enumerate(area_list):
        shuffled_image.paste(tile_list[i], (int(area[0]), int(area[1])))

    return shuffled_image


if __name__ == "__main__":
    image_shuffler('christmas.jpg', 3)


bp = Blueprint("image_shuffle", __name__, url_prefix="/activities/image_shuffle")


@bp.route("/state")
def get_state():
    """Returns image tiles from from provided options"""
    image = request.files.get('image_file', 'christmas.jpg')
    num_tiles = request.args.get("num_tiles", 9)

    # TODO save image and give path to image shuffler function
    image_path = 'christmas.jpg'

    shuffled_image_path, w_num_tiles, h_num_tiles = image_shuffler(image_path, num_tiles)

    return {
        "description": [
            f"Recreate the original image by shuffling the tiles and draw the original image in the empty box or"
            "write the corresponding tile numbers"
        ],
        # TODO how to pass back image?
        "tiles": shuffled_image_path,
        "w_num_tiles": w_num_tiles,
        "h_num_tiles": h_num_tiles
    }

    # TODO delete the image and shuffled image
