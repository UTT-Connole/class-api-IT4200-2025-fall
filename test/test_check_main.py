def test_no_more_than_one_main():
    with open("app.py", "r") as file:
        lines = file.readlines()

    count = 0
    for line in lines:
        if line.strip().startswith("def main"):
            count += 1


    assert count <= 1, f"Found {count} main functions, but should be 1 or less."
