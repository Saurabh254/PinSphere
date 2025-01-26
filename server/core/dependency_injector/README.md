# Injectables - asyncpg and redis


Inject AsyncPG Session
======================

A Python decorator to inject an `AsyncSession` into a coroutine function seamlessly.

Overview
--------

This package provides a decorator, `@inject_asyncpg_session`, that allows you to easily inject an `AsyncSession` into your coroutine functions. This is particularly useful for managing database sessions in asynchronous applications.

Installation
------------

Install the package using pip:

```bash
pip install inject-asyncpg-session
```

Usage
-----

Here's a basic example of how to use the `@inject_asyncpg_session` decorator:

```python
from inject_asyncpg_session import inject_asyncpg_session
from sqlalchemy.ext.asyncio import AsyncSession

@inject_asyncpg_session
async def my_function(session: AsyncSession = Inject()):
    # Use the session here
    ...
```

Key Features
------------

- **Asynchronous Support:** Designed for modern Python async applications.
- **Session Injection:** Simplifies passing `AsyncSession` instances to coroutine functions.
- **Decorator-based:** Intuitive and clean syntax for enhancing functions.

API Reference
-------------

### `@inject_asyncpg_session`

#### Description

Decorator to inject an `AsyncSession` into the decorated coroutine function.

#### Returns

- `Callable`: A decorator that injects an `AsyncSession` into the decorated coroutine function.

#### Example Usage

```python
@inject_asyncpg_session
async def my_function(session: AsyncSession = Inject()):
    # Perform database operations with the injected session
    ...
```

Contributing
------------

Contributions are welcome! If you have suggestions or find issues, feel free to open a pull request or an issue on [GitHub](https://github.com/yourusername/inject-asyncpg-session).

License
-------

This project is licensed under the MIT License. See the LICENSE file for more details.

Author
------

[Saurabh vishwakarma](https://github.com/saurabh254)
```
