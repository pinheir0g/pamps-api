import pytest

@pytest.mark.order(1)
def test_follow_user2(api_client_user2):
    """User2 Follows user1"""

    response = api_client_user2.post(
        "/user/follow/{id}",
        json={"to_user_id": 1})
    assert response.status_code == 201

@pytest.mark.order(2)
def test_timeline_user2(api_client_user2):
    """Timeline user2"""
    
    response = api_client_user2.get("/user/timeline")
    assert response.status_code == 200
    result = response.json()
    assert result[0]["user_id"] == 1
    assert result[0]["text"] == "hello test 1"
    assert result[0]["parent_id"] == None
