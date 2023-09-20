from collections.abc import Hashable, Sequence
from typing import Any


def extract_nested_value(from_obj: dict, keys: Sequence[Hashable], strict=False) -> Any:
    """
    Extract a nested value from a json-like dictionary object.

    Args:
        from_obj: The json-like dictionary to extract the nested value from.
        keys: A sequence of keys to traverse the nested structure.
        strict: When set to False, returns None in case of absence the sequence of keys in a nested structure
            When set to True, raises a KeyError in such a case

    Returns:
        Any: The nested value, or None if it could not be found.

    Raises:
        KeyError: when `strict` is True and the sequence of keys is absent in a nested structure
    """
    nested_obj: Any = from_obj

    if not strict:
        for key in keys:
            try:
                nested_obj = nested_obj.get(key)
            except AttributeError:
                return None

    else:  # strict
        for key in keys:
            if isinstance(nested_obj, str):
                raise KeyError(
                    f"Reached 'str' nested object '{nested_obj}' "
                    f"in object '{from_obj}' while looking for keys '{keys}'"
                )
            else:
                try:
                    nested_obj = nested_obj[key]
                except KeyError as key_error:
                    raise KeyError(
                        f"Keys sequence '{keys}' do not exists in object '{from_obj}'"
                    ) from key_error

    return nested_obj
