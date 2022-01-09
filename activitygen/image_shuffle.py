from flask import Blueprint, request, send_file
from PIL import Image
import random
import math
from io import BytesIO, StringIO


def image_shuffler(image_file, num_tiles):
    # Opens image from given file path
    try:
        original_img = Image.open(image_file)
    except IOError:
        print("No image found at filepath")
        original_img = Image.open('christmas.jpg')
        pass

    width, height = original_img.size

    grid_shuffled = [1]
    grid_solution = [1]

    # If number of tiles is greater than 1, splits into tiles and concatenates shuffles tiles into another image
    if num_tiles > 1:
        # Calculates the optimum splits for each side of the puzzle to keep tiles most square like
        (num_w_tiles, num_h_tiles) = calc_num_splits_on_each_side(width, height, num_tiles)

        # Splits images into tiles
        tile_list, area_list = split_into_tiles(width, height, num_w_tiles, num_h_tiles, original_img)

        # Shuffles tiles and combines them into one image
        shuffled_image, grid_shuffled, grid_solution = concatenate_tiles(tile_list, width, height, area_list, num_w_tiles, num_h_tiles)

    # If number of tiles is 1 or less, then return original image
    else:
        shuffled_image = original_img

    # shuffled_image_path = image_file[0:-4] + "_shuffled.jpg"

    # Save shuffled image
    # shuffled_image.save(shuffled_image_path)

    return shuffled_image, grid_shuffled, grid_solution


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


def concatenate_tiles(tiles_list, width, height, area_list, num_w_tiles, num_h_tiles):
    # Create a new image with same width and height as original
    shuffled_image = Image.new('RGB', (width, height))

    # Shuffles tiles
    shuffles_tiles, grid_shuffled, grid_solution = shuffle_tiles_and_return_grids(tiles_list, num_w_tiles, num_h_tiles)

    # Paste in shuffled tiles in the new image
    for i, area in enumerate(area_list):
        shuffled_image.paste(shuffles_tiles[i], (int(area[0]), int(area[1])))

    return shuffled_image, grid_shuffled, grid_solution


def shuffle_tiles_and_return_grids(tile_list, num_w_tiles, num_h_tiles):

    tile_nums = range(1, len(tile_list) + 1)
    shuffled_list = list(zip(tile_list[:], tile_nums))
    shuffled = False
    while not shuffled:
        random.shuffle(shuffled_list)
        for a, b in zip(tile_list, shuffled_list):
            if a == b[0]:
                break
        else:
            shuffled = True

    shuffled_list_unzipped = [list(t) for t in zip(*shuffled_list)]
    shuffled_tiles = shuffled_list_unzipped[0]
    shuffled_tile_nums = shuffled_list_unzipped[1]

    solution_tile_nums = [0] * len(tile_list)
    for i, tile_num in enumerate(shuffled_tile_nums):
        solution_tile_nums[tile_num - 1] = i + 1

    grid_shuffled = [[0] * num_w_tiles for i in range(num_h_tiles)]
    grid_solution = [[0] * num_w_tiles for i in range(num_h_tiles)]
    counter = 0
    for i in range(num_w_tiles):
        for j in range(num_h_tiles):
            grid_solution[j][i] = solution_tile_nums[counter]
            grid_shuffled[j][i] = tile_nums[counter]
            counter = counter + 1

    return shuffled_tiles, grid_shuffled, grid_solution


if __name__ == "__main__":
    shuffled_tiles, grid_shuffled, grid_solution = image_shuffler('christmas.jpg', 9)
    print("Grid Shuffled", grid_shuffled)
    print("Grid Solution", grid_solution)
    print(' , '.join([' '.join(str(c) for c in lst) for lst in grid_shuffled]))


bp = Blueprint("image_shuffle", __name__, url_prefix="/activities/image_shuffle")


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@bp.route("/state", methods=('GET', 'POST'))
def get_state():
    """Returns image tiles from from provided options"""
    image = request.files['image']
    num_tiles = request.form.get("tile_num")

    shuffled_image_path, grid_shuffled, grid_solution = image_shuffler(image, int(num_tiles))

    response = serve_pil_image(shuffled_image_path)
    response.headers['solved_grid'] = ' , '.join([' '.join(str(c) for c in lst) for lst in grid_solution])
    response.headers['shuffled_grid'] = ' , '.join([' '.join(str(c) for c in lst) for lst in grid_shuffled])
    response.headers['access-control-expose-headers'] = "solved_grid,shuffled_grid"

    return response



    # return {
    #     "description": ("Solve the puzzle by shuffling the tiles in the image to recreate the original.\n"
    #                    "Fill in the grid with numbers corresponding to the unshuffled image.\n"
    #                    "Try your best at drawing and colouring the solved image in the empty box!"),
    #     "test": num_tiles,
    #     "name": image.name,
    #     "grid": grid_shuffled
    #     # TODO how to pass back image?
    #     # "image_shuffled": shuffled_image_path,
    #     # "grid_shuffled": grid_shuffled,
    #     # "image_solution": image.path,
    #     # "grid_solution": grid_solution
    # }

    # TODO delete the image and shuffled image
