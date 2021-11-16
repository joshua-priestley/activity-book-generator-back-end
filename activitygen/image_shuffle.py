from flask import Blueprint, request
from PIL import Image


def image_shuffler(original_img_path, num_tiles):
    original_img = Image.open('christmas.jpg')
    try:
        original_img = Image.open(original_img_path)
    except IOError:
        pass
    width, height = original_img.size

    if num_tiles <= 1:
        dst = original_img
    if num_tiles == 2:
        area_list = []
        tile_list = []
        if width >= height:
            area_list.append((0, 0, width / 2, height))
            area_list.append((width/2, 0, width, height))
        else:
            area_list.append((0, 0, width, height / 2))
            area_list.append((0, height / 2, width, height))

        for i, area in enumerate(area_list):
            tile_list.append(original_img.crop(area))

        if width >= height:
            dst = Image.new('RGB', (tile_list[0].width + tile_list[1].width, tile_list[0].height))
            dst.paste(tile_list[1], (0, 0))
            dst.paste(tile_list[0], (tile_list[1].width, 0))

    dst.save(original_img_path[0:-4] + "_shuffled.jpg")


if __name__ == "__main__":
    image_shuffler('christmas.jpg', 2)


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
