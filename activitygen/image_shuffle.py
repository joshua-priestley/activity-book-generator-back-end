from flask import Blueprint, request
from PIL import Image
import random
import math


def image_shuffler(original_img_path, num_tiles):
    # original_img = Image.open('christmas.jpg')

    try:
        original_img = Image.open(original_img_path)
    except IOError:
        pass

    width, height = original_img.size

    if num_tiles > 1:
        (num_w_tiles, num_h_tiles) = calc_num_splits_on_each_side(width, height, num_tiles)

        tile_list, area_list = split_into_tiles(width, height, num_w_tiles, num_h_tiles, original_img)

        shuffled_image = concatenate_tiles(tile_list, width, height, area_list)

    else:
        shuffled_image = original_img

    shuffled_image.save(original_img_path[0:-4] + "_shuffled.jpg")


def calc_num_splits_on_each_side(width, height, num_tiles):

    factors = []
    for whole_number in range(1, int(math.sqrt(num_tiles)) + 1):
        if num_tiles % whole_number == 0:
            factors.append((whole_number, num_tiles // whole_number))

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

    width_splits = [i * width / num_w_t for i in range(0, num_w_t + 1)]
    height_splits = [i * height / num_h_t for i in range(0, num_h_t + 1)]

    for i in range(0, num_w_t):
        for j in range(0, num_h_t):
            area_list.append((width_splits[i], height_splits[j], width_splits[i + 1], height_splits[j + 1]))
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
    # difficulty = Difficulty.from_str(request.args.get("difficulty"), Difficulty.HARD)
    image = request.files.get('image_file', "")
    num_tiles = request.args.get("num_tiles", 9)

    tiles = image_shuffler(image, num_tiles)

    return {
        "description": [
            f"Recreate the original image by shuffling the tiles and draw the original image in the empty box or"
            "write the corresponding tile numbers"
        ],
        "tiles": tiles,
    }
