from typing import Union
import os
import re

from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

# this "images" should be the same as UPLOADED_{same-name}_DEST i.e UPLOADED_IMAGES_DEST
IMAGE_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)
    regex = fr"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def is_file_safe(file: Union[str, FileStorage], folder: str) -> bool:
    filename = _retrieve_filename(file)
    if is_filename_safe(filename):
        image_path = IMAGE_SET.path(filename=filename, folder=folder)
        return os.path.exists(image_path)
    return False


def get_basename(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
