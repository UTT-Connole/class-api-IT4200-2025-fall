import os
import re

EMOJI_SOURCE = "./.venv/lib/python3.13/site-packages/pip/_vendor/rich/_emoji_codes.py"

EXCLUDED_PATHS = {
    "./.venv",
    "site-packages",
    EMOJI_SOURCE,
}

# full Unicode emoji pattern (covers everything to Unicode 15+)
EMOJI_REGEX = re.compile(
    "["
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F700-\U0001F77F"  # alchemical
    "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
    "\U0001FA70-\U0001FAFF"  # extended-A emojis
    "\U00002600-\U000026FF"  # misc emoji symbols
    "\U00002700-\U000027BF"  # dingbats (some emoji)
    "\U0001F1E6-\U0001F1FF"  # regional flags
    "]+",
    flags=re.UNICODE,
)

def load_emojis_from_source(path):
    """Extract emoji characters from the rich _emoji_codes.py file."""
    emojis = set()
    pattern = re.compile(r'":\s*"(.+?)"')  # match the emoji value
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for match in pattern.findall(line):
                emojis.add(match)
    return emojis


def test_no_emojis_in_repo():
    emojis = load_emojis_from_source(EMOJI_SOURCE)
    if not emojis:
        raise RuntimeError(f"No emojis loaded from {EMOJI_SOURCE}")

    emoji_hits = []

    for root, _, files in os.walk("."):
        if any(excluded in root for excluded in EXCLUDED_PATHS):
            continue

        for f in files:
            path = os.path.join(root, f)
            if (
                f.startswith(".")
                or not f.endswith((".py", ".txt", ".md", ".json", ".yaml", ".yml", ".html", ".db", ".csv", ".js"))
                or any(excluded in path for excluded in EXCLUDED_PATHS)
            ):
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, start=1):
                    # check against both the source list and regex
                    if any(e in line for e in emojis) or EMOJI_REGEX.search(line):
                        emoji_hits.append(f"{path}: line {i}: {line.strip()}")

    if emoji_hits:
        print("Emojis detected:")
        for hit in emoji_hits:
            print(hit)
        raise AssertionError(f"{len(emoji_hits)} emoji-containing lines found.")
    else:
        print("No emojis found in repository.")


if __name__ == "__main__":
    try:
        test_no_emojis_in_repo()
    except AssertionError as e:
        print(str(e))
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(2)
