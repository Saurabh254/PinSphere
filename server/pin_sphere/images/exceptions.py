from pin_sphere.base_exception import ServerError


class ImageNotFoundError(ServerError):
    """
    Raised when an image is not found in the database.

    Attributes:
        status_code (int): The HTTP status code to return.
        message (str): The error message
    """
    def __init__(self, status_code: int = 404, message: str = "Image not found"):
        super().__init__(status_code, message)

class ImageAlreadyExistsError(ServerError):
    """
    Raised when an image is already present in the database.

    Attributes:
        status_code (int): The HTTP status code to return.
        message (str): The error message
    """
    def __init__(self, status_code: int = 400, message: str = "Image already exists"):
        super().__init__(status_code, message)
        self.status_code = status_code
        self.message = message
class ImageFormatError(ServerError):
    """
    Raised when an image is not in a supported format.

    Attributes:
        status_code (int): The HTTP status code to return.
        message (str): The error message
    """
    def __init__(self, status_code: int = 400, message: str = "Invalid file format. Only JPG, JPEG, and PNG files are supported."):
        super().__init__(status_code, message)
