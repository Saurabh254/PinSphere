from pin_sphere.base_exception import ServerError

class ContentNotFoundError(ServerError):
    """
    Raised when content is not found.
    """
    def __init__(self, status_code: int = 404, message: str = "Content not found"):
        super().__init__(status_code, message)

class ContentAlreadyExistsError(ServerError):
    """
    Raised when content already exists.
    """
    def __init__(self, status_code: int = 400, message: str = "Content already exists"):
        super().__init__(status_code, message)

class ContentFormatError(ServerError):
    """
    Raised for unsupported content formats.
    """
    def __init__(self, status_code: int = 400, message: str = "Invalid format. Supported: JPG, JPEG, PNG"):
        super().__init__(status_code, message)
