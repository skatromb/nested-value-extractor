"""Extract a nested value from a json-like dictionary object."""
from collections.abc import Sequence
from typing import Optional, SupportsIndex, TypeGuard, get_args

Key = SupportsIndex
# `Optional` stands for `null` values
JSONValue = Optional[str | int | float | bool]
NestedJSON = dict | list
KEY_ERROR_MSG = 'Keys sequence "{keys}" do not exists in object "{json_obj}"'


class StopExtractionError(Exception):
    """Extraction reached the end of nesting, but keys are not over yet."""


def extract_nested_value(
    json_obj: NestedJSON,
    keys: Sequence[Key],
    safe=True,
) -> JSONValue | NestedJSON:
    """
    Extract a nested value from a json-like dictionary object.

    Args:
        json_obj: The json-like dictionary to extract the nested value from.
        keys: A sequence of keys to traverse the nested structure.
        safe: When set to True, returns None
            in case of absence the sequence of keys in a nested structure
            When set to False, raises a KeyError in such a case

    Returns:
        Any: The nested value, or None if it could not be found.

    Raises:
        KeyError: when `safe` is False
            and the sequence of keys is absent in a nested structure
    """
    nested_obj: JSONValue | NestedJSON = json_obj

    for key in keys:
        try:
            nested_obj = _extract_or_stop(nested_obj, key)
        except StopExtractionError:
            if safe:
                return None
            raise KeyError(
                KEY_ERROR_MSG.format(keys=keys, json_obj=json_obj),
            )

    return nested_obj


def _extract_or_stop(
    nested_obj: JSONValue | NestedJSON,
    key: Key,
) -> JSONValue | NestedJSON:
    """Extract element from `nested_obj` by `key` index.

    Args:
        nested_obj: JSON object (nested or final)
            to get the nested element by indexing
        key: key for indexing the `nested_obj`

    Returns:
        Either another nested JSON or final JSON value

    Raises:
        StopExtractionError: when element is not found

    """
    if _is_nested(nested_obj):
        try:
            return nested_obj[key]
        except (KeyError, TypeError):
            raise StopExtractionError()

    raise StopExtractionError()


def _is_nested(json_obj: JSONValue | NestedJSON) -> TypeGuard[NestedJSON]:
    return isinstance(json_obj, get_args(NestedJSON))
