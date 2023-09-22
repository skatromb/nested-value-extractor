"""Tests for nested_value_extractor"""
import pytest

from src.nested_value_extractor import extract_nested_value


class TestExtractNestedValue:
    """Test suite for nested_value_extractor"""

    def test_extract_nested_value_single_key(self):
        """Extracts a nested value from a dictionary with a single key."""
        from_obj = {1: 2}
        keys = [1]
        expected = 2

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_multiple_keys(self):
        """Extracts a nested value from a dictionary with multiple keys."""
        from_obj = {1: {2: {3: "value"}}}
        keys = [1, 2, 3]
        expected = "value"

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_empty_keys(self):
        """Returns the original dictionary when an empty list of keys is provided."""
        from_obj = {1: 2}
        keys = []
        expected = from_obj

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_int_indexing(self):
        """Results in `None` when ending with `int`."""
        from_obj = {1: 2}
        keys = [1, 2]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_non_dict_value(self):
        """Returns None when a ending with `str`."""
        from_obj = {1: "value"}
        keys = [1, 2]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_str_indexing(self):
        """Returns `None` when ending with `list`."""
        from_obj = {1: [1, 2]}
        keys = [1, 0]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_nonexistent_key_nonstrict(self):
        """Returns None when a non-existent key is provided in a non-safe mode."""
        from_obj = {1: 2}
        keys = ["a"]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_nonexistent_key_strict(self):
        """Raises a NonDictNestedError when a non-existent key is provided in a safe mode."""
        from_obj = {1: 2}
        keys = ["a"]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    def test_extract_nested_value_non_dict_value_strict(self):
        """Raises a KeyError when a non-dict value is encountered while traversing the nested dictionary in safe mode."""
        from_obj = {1: "value"}
        keys = [1, 2]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    def test_extract_nested_value_too_long_keys_strict(self):
        """Raises a KeyError when len(keys) is more than nesting of a dict in a safe mode."""
        from_obj = {1: {2: "value"}}
        keys = [1, 2, 3]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    def test_extract_nested_value_non_dict_input(self):
        """Returns None when a non-dict value is provided as the input dictionary."""
        from_obj = "not a dict"
        keys = [1, 2, 3]
        expected = None

        result = extract_nested_value(from_obj, keys)

        assert result == expected

    def test_extract_nested_value_non_dict_input_strict(self):
        """Raises KeyError when a non-dict value is provided as the input dictionary in safe mode."""
        from_obj = "not a dict"
        keys = [1, 2, 3]
        safe = False

        with pytest.raises(KeyError):
            extract_nested_value(from_obj, keys, safe=safe)

    def test_extract_nested_value_non_sequence_keys(self):
        """Raises TypeError when a non-sequence object is provided as the input keys."""
        from_obj = {1: 2}
        keys = 100
        expected = None

        with pytest.raises(TypeError):
            extract_nested_value(from_obj, keys, expected)

    def test_extract_nested_value_non_hashable_key(self):
        """Raises TypeError when any key in keys is unhashable."""
        from_obj = {1: 2}
        keys = [[1]]

        with pytest.raises(TypeError):
            extract_nested_value(from_obj, keys)
