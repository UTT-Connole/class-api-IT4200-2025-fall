import re

def test_emoji_removed(client):
    from app import users
    users["user1"] = {"balance": 100}  # ensure valid test user

    response = client.post('/slots', json={"bet": 1, "username": "user1"})
    assert response.status_code == 200, f"Unexpected status: {response.status_code}"

    data = response.get_json()
    result = data.get("result", [])
    assert isinstance(result, list), "Result should be a list"

    import re
    emoji_pattern = re.compile(r"[^\x00-\x7F]")
    for symbol in result:
        assert not emoji_pattern.search(symbol), f"Emoji found in symbol: {symbol}"
