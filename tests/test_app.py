import pytest
from httpx import AsyncClient
from fastapi import status
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange: create test client
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: make GET request to /activities
        response = await ac.get("/activities")
    # Assert: check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Arrange: create test client
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act: sign up
        signup_resp = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        # Assert: signup successful
        assert signup_resp.status_code == status.HTTP_200_OK
        assert f"Signed up {test_email}" in signup_resp.json()["message"]
        # Act: try duplicate signup
        dup_resp = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        # Assert: duplicate signup rejected
        assert dup_resp.status_code == status.HTTP_400_BAD_REQUEST
        # Act: unregister
        del_resp = await ac.delete(f"/activities/{activity}/unregister?email={test_email}")
        # Assert: unregister successful
        assert del_resp.status_code == status.HTTP_200_OK
        assert f"Removed {test_email}" in del_resp.json()["message"]
        # Act: unregister again
        del_resp2 = await ac.delete(f"/activities/{activity}/unregister?email={test_email}")
        # Assert: unregister not found
        assert del_resp2.status_code == status.HTTP_404_NOT_FOUND
