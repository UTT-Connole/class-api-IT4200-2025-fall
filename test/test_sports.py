import re
import pytest
from app import app  # assuming app is created at import time

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_sports_status_code(client):
    resp = client.get("/sports")
    assert resp.status_code == 200

def test_sports_json_or_html(client):
    resp = client.get("/sports")
    # Accept either JSON (API style) or HTML (page with form)
    if resp.is_json:
        data = resp.get_json()
        assert "matchup" in data
        assert "winner" in data
        assert "won_bet" in data
    else:
        text = resp.get_data(as_text=True)
        assert "Matchup:" in text or "<form" in text  # basic HTML sanity check

    # HTML path: parse teams from the page, then POST to get the result (session is preserved)
    text = resp.get_data(as_text=True)
    m = re.search(r"Matchup:\s*([A-Za-z0-9' \-\.]+)\s+vs\s+([A-Za-z0-9' \-\.]+)", text)
    assert m, "Could not parse matchup from HTML response"
    team1, team2 = m.group(1).strip(), m.group(2).strip()
    assert team1 and team2 and team1 != team2

    # Place a bet (pick team1) to trigger the POST result; session must be preserved by the test client
    post = client.post("/sports", data={"bet": team1})
    assert post.status_code == 200

    if post.is_json:
        pdata = post.get_json()
        winner = pdata.get("winner")
    else:
        ptext = post.get_data(as_text=True)
        pm = re.search(r"Winner:\s*([A-Za-z0-9' \-\.]+)", ptext)
        assert pm, "Could not parse winner from POST HTML response"
        winner = pm.group(1).strip()

    assert winner in (team1, team2)
# filepath: /home/porte/class-api-IT4200-2025-fall/test/test_sports.py
import re
import pytest
from app import app  # assuming app is created at import time

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_sports_status_code(client):
    resp = client.get("/sports")
    assert resp.status_code == 200

def test_sports_json_or_html(client):
    resp = client.get("/sports")
    # Accept either JSON (API style) or HTML (page with form)
    if resp.is_json:
        data = resp.get_json()
        assert "matchup" in data
        assert "winner" in data
        assert "won_bet" in data
    else:
        text = resp.get_data(as_text=True)
        assert "Matchup:" in text or "<form" in text  # basic HTML sanity check
