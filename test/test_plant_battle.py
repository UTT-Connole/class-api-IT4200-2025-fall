def test_defaults_work(client):
    resp = client.get("/plant-battle?plant=Cactus")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "chosen_plant" in data
    assert "winner" in data
    assert "winnings" in data


def test_invalid_bet_returns_error(client):
    resp = client.get("/plant-battle?bet=0&plant=Cactus")
    assert resp.status_code == 400


def test_invalid_plant_returns_error(client):
    resp = client.get("/plant-battle?bet=10&plant=OakTree")
    assert resp.status_code == 400


def test_valid_request_returns_result(client):
    resp = client.get("/plant-battle?bet=10&plant=Cactus")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "winner" in data
    assert "result" in data
    assert "winnings" in data


def test_outcome_is_win_or_lose(client):
    resp = client.get("/plant-battle?bet=5&plant=Cactus")
    data = resp.get_json()
    assert data["result"] in ["win", "lose"]


def test_message_is_present(client):
    resp = client.get("/plant-battle?bet=10&plant=Cactus")
    data = resp.get_json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 5


def test_environment_and_weather_present(client):

    resp = client.get("/plant-battle?bet=10&plant=Cactus")
    data = resp.get_json()
    assert "battle_environment" in data
    assert "weather" in data
    assert isinstance(data["battle_environment"], str)
    assert isinstance(data["weather"], str)


def test_stats_objects_exist_and_contain_expected_keys(client):
    resp = client.get("/plant-battle?bet=10&plant=Sunflower")
    data = resp.get_json()

    for key in ["chosen_stats", "winner_stats"]:
        assert key in data
        stats = data[key]
        assert "attack" in stats
        assert "defense" in stats
        assert "rarity" in stats
        assert isinstance(stats["attack"], int)
        assert isinstance(stats["defense"], int)
        assert isinstance(stats["rarity"], str)


def test_message_changes_on_win_or_lose(client):
    import random
    win_msgs = set()
    lose_msgs = set()
    # Use a fixed seed to ensure both win and lose outcomes are observed
    for i in range(10):
        random.seed(i)
        resp = client.get("/plant-battle?bet=5&plant=Bamboo")
        data = resp.get_json()
        if data["result"] == "win":
            win_msgs.add(data["message"])
        else:
            lose_msgs.add(data["message"])
    assert len(win_msgs) >= 1
    assert len(lose_msgs) >= 1


def test_environment_and_weather_are_from_known_options(client):
    valid_envs = {"Greenhouse", "Jungle", "Desert", "Swamp", "Backyard"}
    valid_weather = {"Sunny", "Rainy", "Windy", "Cloudy"}

    resp = client.get("/plant-battle?bet=20&plant=Poison%20Ivy")
    data = resp.get_json()
    assert data["battle_environment"] in valid_envs
    assert data["weather"] in valid_weather
