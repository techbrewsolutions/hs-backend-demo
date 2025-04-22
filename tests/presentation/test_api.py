import pytest
from fastapi.testclient import TestClient

from src.presentation.api import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
