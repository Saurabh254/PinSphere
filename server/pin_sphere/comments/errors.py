from pin_sphere.base_exception import ServerError


class CommentNotFoundError(ServerError):
    """
    Raised when a comment cannot be found
    """
    def __init__(self,message: str ="Comment not found", status_code=404  ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.status_code, self.message)
