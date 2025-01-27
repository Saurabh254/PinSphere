from pin_sphere.base_exception import ServerError


class UserNotFound(ServerError):
    def __init__(self, status_code: int = 404, message: str = 'User not found'):
        super().__init__(status_code, message)
        self.status_code = status_code
        self.message = message


class InvalidUsernameOrPassword(ServerError):
    def __init__(self, message: str = 'Invalid username or password'):
        super().__init__(400, message)
        self.status_code = 400
        self.message = message

class UserAlreadyExists(ServerError):
    def __init__(self, message: str = 'User already exists'):
        super().__init__(400, message)
        self.status_code = 400
        self.message = message
