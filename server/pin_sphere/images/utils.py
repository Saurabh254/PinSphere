import uuid

from core.types import FileContentType


def get_image_key(username: str, ext: FileContentType) -> str :
    """
    Generate a unique image key for the given username and extension.

    Args:
        username (str): The username of the user.
        ext (str): The file extension of the image.

    Returns:
        str: The generated image key
    """
    return f"images/{username}/{uuid.uuid4()}.{ext.name.casefold()}"
