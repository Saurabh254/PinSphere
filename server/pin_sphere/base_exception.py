from typing import Literal

from pydantic import BaseModel, create_model


class ServerError(Exception):
    def __init__(
        self,
        status_code: int = 500,
        message: str = "unexpected error occurred",
        headers: dict[str, str] | None = {},
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers

    @classmethod
    def schema(cls) -> type[BaseModel]:
        type_literal = Literal[cls.__name__]  # type: ignore

        return create_model(cls.__name__, type=(type_literal, ...), detail=(str, ...))


class ResourceNotFound(ServerError):
    def __init__(self, message: str = "Not found", status_code: int = 404) -> None:
        super().__init__(message=message, status_code=status_code)


class UnauthorisedUser(ServerError):
    def __init__(self, message: str = "unauthorised", status_code: int = 401) -> None:
        super().__init__(message=message, status_code=status_code)


class InvalidSession(ServerError):
    def __init__(
        self, message: str = "invalid session", status_code: int = 403
    ) -> None:
        super().__init__(message=message, status_code=status_code)
