import pytest

from src.nested_dict_extractor import extract_nested_value, KeyNestedError


class TestExtractNestedValue:

    #  Extracts a nested value from a dictionary with a single key.
    def test_extract_nested_value_single_key(self):
        from_dict = {1: 2}
        keys = [1]
        expected = 2

        result = extract_nested_value(from_dict, keys)

        assert result == expected

    #  Extracts a nested value from a dictionary with multiple keys.
    def test_extract_nested_value_multiple_keys(self):
        from_dict = {1: {2: {3: "value"}}}
        keys = [1, 2, 3]
        expected = "value"

        result = extract_nested_value(from_dict, keys)

        assert result == expected

    #  Returns the original dictionary when an empty list of keys is provided.
    def test_extract_nested_value_empty_keys(self):
        from_dict = {1: 2}
        keys = []
        expected = from_dict

        result = extract_nested_value(from_dict, keys)

        assert result == expected

    #  Returns None when a non-existent key is provided in a non-strict mode.
    def test_extract_nested_value_nonexistent_key_nonstrict(self):
        from_dict = {1: 2}
        keys = ["a"]
        expected = None

        result = extract_nested_value(from_dict, keys)

        assert result == expected

    #  Raises a NonDictNestedError when a non-existent key is provided in a strict mode.
    def test_extract_nested_value_nonexistent_key_strict(self):
        from_dict = {1: 2}
        keys = ["a"]
        strict = True

        with pytest.raises(KeyNestedError):
            extract_nested_value(from_dict, keys, strict=strict)

    #  Raises a ValueError when a non-dict value is encountered while traversing the nested dictionary.
    def test_extract_nested_value_non_dict_value(self):
        from_dict = {1: "value"}
        keys = [1, 2]
        strict = True

        with pytest.raises(ValueError):
            extract_nested_value(from_dict, keys, strict=strict)

    #  Raises a ValueError when len(keys) is more than nesting of a dict in a strict mode.
    def test_extract_nested_value_too_long_keys_strict(self):
        from_dict = {1: {2: "value"}}
        keys = [1, 2, 3]
        strict = True

        with pytest.raises(ValueError):
            extract_nested_value(from_dict, keys, strict=strict)

    #  Returns None when a non-dict value is provided as the input dictionary.
    def test_extract_nested_value_non_dict_input(self):
        from_dict = "not a dict"
        keys = [1, 2, 3]
        expected = None

        result = extract_nested_value(from_dict, keys)

        assert result == expected

    #  Raises ValueError when a non-dict value is provided as the input dictionary in strict mode.
    def test_extract_nested_value_non_dict_input_strict(self):
        from_dict = "not a dict"
        keys = [1, 2, 3]
        strict = True

        with pytest.raises(ValueError):
            extract_nested_value(from_dict, keys, strict=strict)

    #  Raises ValueError when a non-sequence object is provided as the input keys.
    def test_extract_nested_value_non_sequence_keys(self):
        from_dict = {1: 2}
        keys = 100
        expected = None

        with pytest.raises(ValueError):
            extract_nested_value(from_dict, keys, expected)

    #  Raises ValueError when any key in keys is unhashable.
    def test_extract_nested_value_non_hashable_key(self):
        from_dict = {1: 2}
        keys = [[1]]

        with pytest.raises(ValueError):
            extract_nested_value(from_dict, keys)
