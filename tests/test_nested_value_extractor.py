import pytest

from src.nested_value_extractor import extract_nested_value


class TestExtractNestedValue:
    #  Extracts a nested value from a dictionary with a single key.
    def test_extract_nested_value_single_key(self):
        from_obj = {1: 2}
        keys = [1]
        expected = 2

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Extracts a nested value from a dictionary with multiple keys.
    def test_extract_nested_value_multiple_keys(self):
        from_obj = {1: {2: {3: "value"}}}
        keys = [1, 2, 3]
        expected = "value"

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Returns the original dictionary when an empty list of keys is provided.
    def test_extract_nested_value_empty_keys(self):
        from_obj = {1: 2}
        keys = []
        expected = from_obj

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Results in `None` when ending with `int`.
    def test_extract_nested_value_int_indexing(self):
        from_obj = {1: 2}
        keys = [1, 2]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Returns None when a ending with `str`.
    def test_extract_nested_value_non_dict_value(self):
        from_obj = {1: "value"}
        keys = [1, 2]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Returns `None` when ending with `list`.
    def test_extract_nested_value_str_indexing(self):
        from_obj = {1: [1, 2]}
        keys = [1, 0]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Returns None when a non-existent key is provided in a non-safe mode.
    def test_extract_nested_value_nonexistent_key_nonstrict(self):
        from_obj = {1: 2}
        keys = ["a"]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Raises a NonDictNestedError when a non-existent key is provided in a safe mode.
    def test_extract_nested_value_nonexistent_key_strict(self):
        from_obj = {1: 2}
        keys = ["a"]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    #  Raises a KeyError when a non-dict value is encountered while traversing the nested dictionary in safe mode.
    def test_extract_nested_value_non_dict_value_strict(self):
        from_obj = {1: "value"}
        keys = [1, 2]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    #  Raises a KeyError when len(keys) is more than nesting of a dict in a safe mode.
    def test_extract_nested_value_too_long_keys_strict(self):
        from_obj = {1: {2: "value"}}
        keys = [1, 2, 3]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    #  Returns None when a non-dict value is provided as the input dictionary.
    def test_extract_nested_value_non_dict_input(self):
        from_obj = "not a dict"
        keys = [1, 2, 3]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    #  Raises KeyError when a non-dict value is provided as the input dictionary in safe mode.
    def test_extract_nested_value_non_dict_input_strict(self):
        from_obj = "not a dict"
        keys = [1, 2, 3]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    #  Raises TypeError when a non-sequence object is provided as the input keys.
    def test_extract_nested_value_non_sequence_keys(self):
        from_obj = {1: 2}
        keys = 100
        expected = None

        with pytest.raises(TypeError):
            extract_nested_value(from_obj, keys, expected)

    #  Raises TypeError when any key in keys is unhashable.
    def test_extract_nested_value_non_hashable_key(self):
        from_obj = {1: 2}
        keys = [[1]]

        with pytest.raises(TypeError):
            extract_nested_value(from_obj, keys)
