__all__ = ["test_client"]
from fastapi.testclient import TestClient
from main import app


test_client = TestClient(app, base_url="http://testclient/api/v1")
