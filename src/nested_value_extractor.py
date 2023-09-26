"""Extract a nested value from a json-like dictionary object."""
from collections.abc import Hashable, Sequence
from typing import Any

Keys = Sequence[Hashable]


def extract_nested_value(
    from_obj: dict,
    keys: Keys,
    safe=True,
) -> Any:
    """
    Extract a nested value from a json-like dictionary object.

    Args:
        from_obj: The json-like dictionary to extract the nested value from.
        keys: A sequence of keys to traverse the nested structure.
        safe: When set to True, returns None
            in case of absence the sequence of keys in a nested structure
            When set to False, raises a KeyError in such a case

    Returns:
        Any: The nested value, or None if it could not be found.

    Raises:
        KeyError: when `safe_mode` is False
            and the sequence of keys is absent in a nested structure
    """
    nested_obj: Any = from_obj

    if safe:
        for key in keys:
            try:
                nested_obj = nested_obj.get(key)
            except AttributeError:
                nested_obj = None

    else:  # safe
        for key in keys:
            string = isinstance(nested_obj, str)
            not_indexable = not hasattr(nested_obj, "__getitem__")
            if string or not_indexable:
                raise KeyError(
                    (
                        'Keys sequence "{keys}" do not exists ' +
                        'in object "{from_obj}"'
                    ).format(keys=keys, from_obj=from_obj),
                )
            nested_obj = nested_obj[key]

    return nested_obj
