import re

# Regular expression that matches most common emoji ranges
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002700-\U000027BF"  # dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)

def test_emojis(client):
    """
    Ensures all key API endpoints return responses with no emojis.
    """
    endpoints = ["/api/v1/status", "/api/v1/users", "/api/v1/items"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        body = response.text

        # Fail if any emoji characters are found
        assert not EMOJI_PATTERN.search(body), f"Emoji found in response for {endpoint}"
