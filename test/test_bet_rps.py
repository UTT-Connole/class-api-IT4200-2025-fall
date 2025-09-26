import random

#def test_bet_rps_outcomes(client, monkeypatch):
#    scenarios = [
#        ("rock", "scissors", 200, "win"),     # win
#        ("paper", "paper", 100, "tie"),       # tie
#        ("scissors", "rock", 0, "lose"),      # lose
#    ]
#
#    for player, comp, payout, outcome in scenarios:
#        monkeypatch.setattr(random, "choice", lambda _: comp)
#        resp = client.get(f"/bet_rps?player={player}&amount=100")
#        data = resp.get_json()
#        assert resp.status_code == 200
#        assert data["outcome"] == outcome
#        assert data["payout"] == payout


# def test_bet_rps_invalid(client):
#     for url in ["/bet_rps?player=lizard&amount=10", "/bet_rps?player=rock&amount=0"]:
#         resp = client.get(url)
#         data = resp.get_json()
#         assert resp.status_code == 400
#         assert data["error"] == "Invalid move or amount"
