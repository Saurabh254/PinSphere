from typing import Optional

from pydantic import BaseModel
from pin_sphere.base_exception import ServerError
import logging


class CacheInitilizationError(ServerError):

    def __init__(
        self, namespace: Optional[str] = None, entity: Optional[BaseModel] = None
    ) -> None:
        logging.critical(
            f"Failed to initilize the CacheManager class with the namespace [{namespace}] and entity [{entity}]"
        )
        super().__init__()


class InvalidEntity(CacheInitilizationError):
    def __init__(
        self, namespace: str | None = None, entity: BaseModel | None = None
    ) -> None:
        super().__init__(namespace, entity)
