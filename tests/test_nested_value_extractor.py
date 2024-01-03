"""Tests for nested_value_extractor."""
from typing import Sequence

import pytest

from src.nested_value_extractor import (
    JSONValue,
    Key,
    NestedJSON,
    extract_nested_value,
)

NON_HAPPY_ARGS = (
    ({1: "string shouldn't be indexed"}, [1, 2]),
    ({1: 2}, [1, 'end of nesting reached']),
    ({1: 2}, ['non existent key']),
    (1, ['non-indexable object']),
    ({1: 'nested key fail'}, [[1]]),
)


@pytest.mark.parametrize('safe', [True, False])
@pytest.mark.parametrize(
    'json_obj, keys, expected',
    [
        ({1: '1-st level value'}, [1], '1-st level value'),
        ({1: {2: {3: '3-rd level value'}}}, [1, 2, 3], '3-rd level value'),
        ({'no keys in': 'same dict out'}, [], {'no keys in': 'same dict out'}),
    ],
)
def test_happy_ways(
    json_obj: dict,
    keys: Sequence[Key],
    safe: bool,
    expected: NestedJSON | JSONValue,
) -> None:
    """Tests happy ways."""
    assert extract_nested_value(json_obj, keys, safe) == expected


@pytest.mark.parametrize(
    'json_obj, keys, expected',
    [(*args, None) for args in NON_HAPPY_ARGS],
)
def test_not_found_safe(
    json_obj: dict,
    keys: Sequence[Key],
    expected: None,
) -> None:
    """Tests cases when keys sequence is not found."""
    assert extract_nested_value(json_obj, keys) is expected


@pytest.mark.parametrize('safe', [False])
@pytest.mark.parametrize(
    'json_obj, keys',
    NON_HAPPY_ARGS,
)
def test_exceptions(
    json_obj: dict,
    keys: Sequence[Key],
    safe: bool,
):
    """Tests cases when keys sequence is not found and exception is thrown."""
    with pytest.raises(KeyError):
        extract_nested_value(json_obj, keys, safe)
