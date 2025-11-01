# filepath: test/test_sports.py
import re
import pytest
from app import app  # assuming app is created at import time


@pytest.fixture
def client():
    with app.test_client() as test_client:
        yield test_client


def test_sports_league_switch(client):
    # Define expected team sets
    nfl_teams = {
        "49ers", "Bears", "Bengals", "Bills", "Broncos", "Browns", "Buccaneers",
        "Cardinals", "Chargers", "Chiefs", "Colts", "Commanders", "Cowboys",
        "Dolphins", "Eagles", "Falcons", "Giants", "Jaguars", "Jets", "Lions",
        "Packers", "Panthers", "Patriots", "Raiders", "Rams", "Ravens",
        "Saints", "Seahawks", "Steelers", "Texans", "Titans", "Vikings"
    }
    nba_teams = {
        "Hawks", "Celtics", "Nets", "Hornets", "Bulls", "Cavaliers", "Mavericks",
        "Nuggets", "Pistons", "Warriors", "Rockets", "Pacers", "Clippers",
        "Lakers", "Grizzlies", "Heat", "Bucks", "Timberwolves", "Pelicans",
        "Knicks", "Thunder", "Magic", "76ers", "Suns", "Trail Blazers", "Kings",
        "Spurs", "Raptors", "Jazz", "Wizards"
    }

    # 1) Test NFL
    resp_nfl = client.get("/sports?sport=nfl")
    assert resp_nfl.status_code == 200
    html_nfl = resp_nfl.get_data(as_text=True)
    nfl_match = any(team in html_nfl for team in nfl_teams)
    nba_match = any(team in html_nfl for team in nba_teams)
    assert nfl_match, "Expected NFL team names when sport=nfl"
    assert not nba_match, "Did not expect NBA teams when sport=nfl"


def test_sports_expected_teams(client):
    # Expected AFC and NFC teams
    afc_teams = {
        "Bills", "Dolphins", "Patriots", "Jets",
        "Ravens", "Bengals", "Browns", "Steelers",
        "Texans", "Colts", "Jaguars", "Titans",
        "Broncos", "Chiefs", "Raiders", "Chargers"
    }
    nfc_teams = {
        "Cowboys", "Giants", "Eagles", "Commanders",
        "Bears", "Lions", "Packers", "Vikings",
        "Falcons", "Panthers", "Saints", "Buccaneers",
        "Cardinals", "Rams", "49ers", "Seahawks"
    }

    resp = client.get("/sports")
    assert resp.status_code == 200

    html = resp.get_data(as_text=True)
    assert "Matchup:" in html, "Response does not contain a matchup"

    match = re.search(r"Matchup:\s*([A-Za-z0-9' \-\.]+)\s+vs\s+([A-Za-z0-9' \-\.]+)", html)
    assert match, "Could not extract teams from the matchup"
    team1, team2 = match.groups()

    allowed = afc_teams.union(nfc_teams)
    assert team1 in allowed, f"Team {team1} is not in the expected teams"
    assert team2 in allowed, f"Team {team2} is not in the expected teams"


def test_reset_button(client):
    # First GET request to get the initial matchup
    resp1 = client.get("/sports")
    assert resp1.status_code == 200
    text1 = resp1.get_data(as_text=True)

    # Extract the initial matchup
    match1 = re.search(r"Matchup:\s*([A-Za-z0-9' \-\.]+)\s+vs\s+([A-Za-z0-9' \-\.]+)", text1)
    assert match1, "Could not find initial matchup in response"
    team1_initial, team2_initial = match1.groups()

    # GET request with reset=true to reset the matchup
    resp2 = client.get("/sports?reset=true")
    assert resp2.status_code == 200
    text2 = resp2.get_data(as_text=True)

    # Extract the new matchup
    match2 = re.search(r"Matchup:\s*([A-Za-z0-9' \-\.]+)\s+vs\s+([A-Za-z0-9' \-\.]+)", text2)
    assert match2, "Could not find new matchup in response after reset"
    team1_new, team2_new = match2.groups()

    # Ensure the matchup has changed
    assert (team1_initial, team2_initial) != (team1_new, team2_new), "Matchup did not reset"


def test_css_in_sports_html():
    with open("templates/sports.html", "r", encoding="utf-8") as file_handle:
        content = file_handle.read()

    has_inline_css = "<style>" in content
    has_external_css = '<link rel="stylesheet"' in content

    assert has_inline_css or has_external_css, "No CSS found in sports.html"


def test_sports_status_code(client):
    resp = client.get("/sports")
    assert resp.status_code == 200


