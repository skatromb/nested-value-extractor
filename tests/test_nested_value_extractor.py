"""Tests for nested_value_extractor."""
from typing import Any

import pytest

from src.nested_value_extractor import Keys, extract_nested_value

NON_HAPPY_ARGS = (
    ({1: "string shouldn't be indexed"}, [1, 2]),
    ({1: 2}, [1, 'end of nesting reached']),
    ({1: 2}, ['non existent key']),
    (1, ['non-indexable object']),
)


@pytest.mark.parametrize('safe', [True, False])
@pytest.mark.parametrize(
    'from_obj, keys, expected',
    [
        ({1: '1-st level value'}, [1], '1-st level value'),
        ({1: {2: {3: '3-rd level value'}}}, [1, 2, 3], '3-rd level value'),
        ({'no keys in': 'same dict out'}, [], {'no keys in': 'same dict out'}),
    ],
)
def test_happy_ways(
    from_obj: dict,
    keys: Keys,
    safe: bool,
    expected: Any,
) -> None:
    """Tests happy ways."""
    assert extract_nested_value(from_obj, keys, safe) == expected


@pytest.mark.parametrize(
    'from_obj, keys, expected',
    [(*args, None) for args in NON_HAPPY_ARGS],
)
def test_not_found_safe(
    from_obj: dict,
    keys: Keys,
    expected: Any,
) -> None:
    """Tests cases when keys sequence is not found."""
    assert extract_nested_value(from_obj, keys) is expected


@pytest.mark.parametrize('safe', [False])
@pytest.mark.parametrize(
    'from_obj, keys, expected_exception',
    [({1: 'nested key fail'}, [[1]], pytest.raises(TypeError))] +
    [(*args, pytest.raises(KeyError)) for args in NON_HAPPY_ARGS],
)
def test_exceptions(
    from_obj: dict,
    keys: Keys,
    safe: bool,
    expected_exception: pytest.ExceptionInfo,
):
    """Tests cases when keys sequence is not found and exception is thrown."""
    with expected_exception:
        extract_nested_value(from_obj, keys, safe)
