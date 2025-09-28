# import json
# from deepdiff import DeepDiff

# expected = {
#     "hand_rankings": [
#         {
#             "rank": 1,
#             "name": "Royal Flush",
#             "description": "Ace, King, Queen, Jack, and Ten, all of the same suit.",
#             "example": "A♥ K♥ Q♥ J♥ 10♥"
#         },
#         {
#             "rank": 2,
#             "name": "Straight Flush",
#             "description": "Five cards in sequence, all of the same suit. A Royal Flush is the highest possible Straight Flush.",
#             "example": "9♠ 8♠ 7♠ 6♠ 5♠"
#         },
#         {
#             "rank": 3,
#             "name": "Four of a Kind",
#             "description": "Four cards of the same rank.",
#             "example": "7♣ 7♠ 7♥ 7♦ 2♣"
#         },
#         {
#             "rank": 4,
#             "name": "Full House",
#             "description": "Three cards of one rank and two cards of another rank.",
#             "example": "Q♣ Q♠ Q♦ J♥ J♣"
#         },
#         {
#             "rank": 5,
#             "name": "Flush",
#             "description": "Five cards of the same suit, not in sequence.",
#             "example": "K♦ J♦ 7♦ 5♦ 3♦"
#         },
#         {
#             "rank": 6,
#             "name": "Straight",
#             "description": "Five cards in sequence, but not of the same suit.",
#             "example": "6♠ 5♠ 4♦ 3♦ 2♥"
#         },
#         {
#             "rank": 7,
#             "name": "Three of a Kind",
#             "description": "Three cards of the same rank.",
#             "example": "8♥ 8♠ 8♦ 5♣ 2♥"
#         },
#         {
#             "rank": 8,
#             "name": "Two Pair",
#             "description": "Two separate pairs of cards of the same rank.",
#             "example": "9♥ 9♣ 5♠ 5♦ 2♦"
#         },
#         {
#             "rank": 9,
#             "name": "One Pair",
#             "description": "Two cards of the same rank.",
#             "example": "A♠ A♣ 8♥ 4♦ 3♥"
#         },
#         {
#             "rank": 10,
#             "name": "High Card",
#             "description": "When a hand does not meet any of the higher ranking combinations, the highest card determines the rank.",
#             "example": "A♣ Q♦ J♠ 9♥ 7♣"
#         }
#     ]
# }


# def test_pokerHandRankings(client):
#     response = client.get('/pokerHandRankings')
#     assert response.status_code == 200

#     data = response.get_json()
#     if data != expected:
#         print("Returned data:")
#         print(json.dumps(data, indent=2, ensure_ascii=False))
#         print("\nExpected data:")
#         print(json.dumps(expected, indent=2, ensure_ascii=False))

    
#     assert data == expected

