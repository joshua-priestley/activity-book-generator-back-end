from flask import Blueprint, request


def image_shuffler(image, num_tiles):
    tiles = [image]
    return tiles


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
