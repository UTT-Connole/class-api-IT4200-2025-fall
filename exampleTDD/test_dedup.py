from dedup import deduplicate

def test_deduplicate_passthrough():
    input_list = [1]
    output_list = deduplicate(input_list)
    assert output_list == [1]


def test_deduplicate_empty():
    input_list = []
    output_list = deduplicate(input_list)
    assert output_list == []


def test_deduplicate_duplicates():
    input_list = [1, 1]
    output_list = deduplicate(input_list)
    assert output_list == [1]


def test_deduplicate_three_ones():
    input_list = [1, 1, 1]
    output_list = deduplicate(input_list)
    assert output_list == [1]

def test_deduplicate_mixed():
    input_list = [1, 1, 2, 2, 3, 3]
    output_list = deduplicate(input_list)
    assert output_list == [1, 2, 3]

def test_unsorted_dedup_list():
    input_list = [3, 1, 2, 3, 2, 1]
    output_list = deduplicate(input_list)
    assert output_list == [3,1,2]


def test_deduplicate_strings():
    input= "hello world"

    output = deduplicate(input)
    assert output == " dummy don't give me strings!!!"