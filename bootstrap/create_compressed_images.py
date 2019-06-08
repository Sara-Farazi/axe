import os

from PIL import Image

DATA_DIR = "data"
ORIGINAL_IMAGES_DIR = "images"
COMPRESSED_IMAGES_DIR = "compressed"

SOURCE_DIR = "{}/{}".format(DATA_DIR, ORIGINAL_IMAGES_DIR)
DEST_DIR = "{}/{}".format(DATA_DIR, COMPRESSED_IMAGES_DIR)

QUALITY_FACTOR = 65


def get_original_file_path(filename):
    return "{}/{}".format(SOURCE_DIR, filename)


def get_compressed_file_path(filename):
    return "{}/{}".format(DEST_DIR, filename)


def compress(file):
    filepath = get_original_file_path(file)
    picture = Image.open(filepath)
    picture.save(get_compressed_file_path(file), "JPEG", optimize=True, quality=QUALITY_FACTOR)


def main():
    if not os.path.isdir(DEST_DIR):
        os.mkdir(DEST_DIR)

    counter = 0
    for file in os.listdir(SOURCE_DIR):
        if counter > 100:
            return
        if os.path.splitext(file)[1].lower() == ".jpg":
            compress(file)
            counter += 1


if __name__ == "__main__":
    main()
