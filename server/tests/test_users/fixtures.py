import asyncio

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from core.database.session_manager import get_async_session
