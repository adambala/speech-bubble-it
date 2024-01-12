from PIL import Image, ImageOps, ImageColor, ImageChops

from argparse import ArgumentParser, BooleanOptionalAction
from pathlib import Path
import os
import logging
import sys

ASSETS_DIR = "assets"
SPEECH_BUBBLE_FILENAME = "speech_bubble.png"

# formats known to be supported
SUPPORTED_FORMATS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".webp",
    ".tiff",
)


def check_file_format(file_path: Path, supported_formats: tuple) -> None:
    """
    Checks if the file extension is supported.
    """

    if file_path.suffix not in supported_formats:
        raise ValueError(
            f"Unsupported file extension {file_path.suffix}. Only {supported_formats} are supported."
        )


def open_image(image_path: Path) -> Image.Image:
    """
    Return an Image object of image.
    """

    with Image.open(image_path) as img:
        img.load()

    return img


def transform_image(img: Image.Image, mirror: bool, orientation: int) -> Image.Image:
    """
    Changes an image according to command arguments.
    """

    if mirror:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    match orientation:
        case 1: pass  # default orientation
        case 2: img = img.transpose(Image.ROTATE_90)
        case 3: img = img.transpose(Image.ROTATE_180)
        case 4: img = img.transpose(Image.ROTATE_270)

    return img


def process(image_path: Path, output_path: Path, mirror: bool, orientation: int) -> None:
    """
    Adds a speech bubble on image and saves it.
    """

    if not image_path.is_file():
        raise FileNotFoundError(f"Image file {image_path} not found")

    check_file_format(image_path, SUPPORTED_FORMATS)
    check_file_format(output_path, SUPPORTED_FORMATS)

    original_image = open_image(image_path).convert(
        "RGBA"  # to ensure transperency in the result
    )
    speech_bubble_image = open_image(
        Path(os.path.join(ASSETS_DIR, SPEECH_BUBBLE_FILENAME))
    )

    # to prevent unexpected rotation of images with EXIF orientation tag != 1
    ImageOps.exif_transpose(original_image, in_place=True)

    speech_bubble_image = speech_bubble_image.resize(original_image.size)
    speech_bubble_image = transform_image(
        speech_bubble_image, mirror, orientation
    )

    result = ImageChops.subtract_modulo(original_image, speech_bubble_image)

    # these formats does not support transperency, so it fills alpha channel with color
    if output_path.suffix in (".jpg", ".jpeg", "bmp"):
        alpha = result.split()[3]
        bg = Image.new("RGB", result.size, ImageColor.getrgb("WHITE"))
        bg.paste(result, mask=alpha)
        result = bg

    if not output_path.parent.is_dir():
        output_path.parent.mkdir(parents=True, exist_ok=True)

    result.save(output_path)
    logging.info(f"Image saved at {output_path.resolve()}")


def main() -> None:
    """
    Initializes command arguments.
    """

    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

    parser = ArgumentParser()
    parser.add_argument("image_path", type=Path, metavar="image_file",
                        help="path of an image you want to put speech bubble on")
    parser.add_argument("output_path", type=Path, metavar="output_file",
                        help="path to the file where the result will be written to")
    parser.add_argument("-m", "--mirror", action=BooleanOptionalAction,
                        help="flips speech bubble horizontally")
    parser.add_argument("-o", "--orientation", type=int, default=1, choices=(1, 2, 3, 4),
                        help="changes speech bubble orientation (1: on the top; 2: on the left; 3: on the bottom; 4: on the right)")
    args = parser.parse_args()

    process(**vars(args))


if __name__ == "__main__":
    main()
