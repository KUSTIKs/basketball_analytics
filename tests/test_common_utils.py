from utils.common_utils import invert_dict


def test_invert_dict_basic():
    d = {"a": 1, "b": 2, "c": 3}
    inverted = invert_dict(d)
    assert inverted == {1: "a", 2: "b", 3: "c"}


def test_invert_dict_empty():
    d = {}
    inverted = invert_dict(d)
    assert inverted == {}


def test_invert_dict_non_str_keys():
    d = {1: "one", 2: "two"}
    inverted = invert_dict(d)
    assert inverted == {"one": 1, "two": 2}


def test_invert_dict_duplicate_values():
    d = {"a": 1, "b": 1}
    inverted = invert_dict(d)
    assert inverted[1] in ("a", "b")
