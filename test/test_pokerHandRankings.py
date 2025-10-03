import json
import jsonschema

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["hand_rankings"],
    "additionalProperties": False,
    "properties": {
        "hand_rankings": {
            "type": "array",
            "minItems": 10,
            "maxItems": 10,
            "items": {
                "type": "object",
                "required": ["rank", "name", "description", "example"],
                "additionalProperties": False,
                "properties": {
                    "rank": {"type": "integer", "minimum": 1, "maximum": 10},
                    "name": {
                        "type": "string",
                        "enum": [
                            "Royal Flush",
                            "Straight Flush",
                            "Four of a Kind",
                            "Full House",
                            "Flush",
                            "Straight",
                            "Three of a Kind",
                            "Two Pair",
                            "One Pair",
                            "High Card"
                        ]
                    },
                    "description": {"type": "string", "minLength": 5},
                    "example": {
                        "type": "string",
                        # 5 tokens like "A♥ K♥ Q♥ J♥ 10♥" - adjust suits/ranks if needed
                        "pattern": r"^(?:A|K|Q|J|10|[2-9])[♥♦♣♠](?:\s(?:A|K|Q|J|10|[2-9])[♥♦♣♠]){4}$"
                    }
                }
            }
        }
    }
}

def test_pokerHandRankings_returns_200(client):
    response = client.get('/pokerHandRankings')
    assert response.status_code == 200

def test_pokerHandRankings_correct_response(client):
    with open('./import_resources/pokerHandRankings.json', 'r') as file:
        expected = json.load(file)

    response = client.get('/pokerHandRankings')
    try:
        jsonschema.validate(instance=response.json, schema=SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        print("Validation error:", e.message)

    data = response.json
    assert data == expected

def test_pokerHandRankings_returns_304_on_non_GET(client):
    response = client.post('/pokerHandRankings')
    assert response.status_code == 405