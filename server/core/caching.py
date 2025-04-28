import json
from typing import Literal, Self, Union, List

from core.baseErrors import CacheInitilizationError, InvalidEntity
from core.models.content import Content
from core.models.user import User
from core.redis_utils import get_redis_client

ENTITY_TYPE = User | Content | List[User | Content]


def retrieve_namespace(namespace: str, entity_id: str) -> str:
    return f"{namespace}_{entity_id}"


class CachingManager:
    _namespace: str | None = None

    def namespace(self, namespace: Literal["User", "Content"]) -> Self:
        self._namespace = namespace
        return self

    async def save(self, entity: ENTITY_TYPE) -> None:
        if self._namespace is None:
            raise CacheInitilizationError(self._namespace, entity)

        if not isinstance(entity, (User, Content, list)):
            raise InvalidEntity(self._namespace, entity)

        redis_conn = await anext(get_redis_client())

        if isinstance(entity, list):
            for item in entity:  # type: ignore
                if not isinstance(item, (User, Content)):
                    raise InvalidEntity(self._namespace, item)  # type: ignore
                if not isinstance(item, (User, Content)):
                    raise InvalidEntity(self._namespace, item)
                key = retrieve_namespace(self._namespace, str(item.id))
                await redis_conn.set(key, json.dumps(item.as_dict()))
        else:
            key = retrieve_namespace(self._namespace, str(entity.id))
            await redis_conn.set(key, json.dumps(entity.as_dict()))

    async def retrieve(
        self, namespace: Literal["User", "Content"], entity_id: str
    ) -> Union[User, Content, None]:
        key = retrieve_namespace(namespace, entity_id)
        redis_conn = await anext(get_redis_client())

        data = await redis_conn.get(key)
        if data is None:
            return None

        obj_data = json.loads(data)

        if namespace == "User":
            return User(**obj_data)
        elif namespace == "Content":
            return Content(**obj_data)

        # This should not happen if Literal["User", "Content"] is correct
        raise InvalidEntity(namespace, obj_data)
