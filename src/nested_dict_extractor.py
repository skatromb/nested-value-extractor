from collections.abc import Hashable, Sequence
from typing import Any


class KeyNestedError(KeyError):
    pass


def extract_nested_value(
    from_dict: dict, keys: Sequence[Hashable], strict=False
) -> Any | None:
    """Derive nested value from dict by providing a sequence of keys
    Args:
        from_dict (dict): The dictionary from which the nested value is extracted.
        keys (Sequence[Hashable]): Ordered sequence of keys to derive the nested value.
        strict (bool, optional): When set to `False`, prevents throwing an exception when keys do not exist in the nested dict.
    Returns:
        Any | None: Nested value if all keys exist, or None.
    Examples:
        >>> extract_nested_value({1: 2}, [1])
        2
        >>> extract_nested_value({1: {2: {3: "value"}}}, [1, 2, 3])
        "value"
        >>> extract_nested_value({1: 2}, ["a"])
        None
        >>> extract_nested_value({1: 2}, ["a"], strict=True)
        Raises

    """
    _initial_from_dict, _initial_keys = from_dict, keys
    if not issubclass(type(keys), Sequence):
        raise ValueError(f"Keys parameter '{keys}' is not a Sequence")
    if any(not issubclass(type(key), Hashable) for key in keys):
        raise ValueError("Some of the keys are not hashable objects")
    return _extract(from_dict, keys, strict, _initial_from_dict, _initial_keys)


def _extract(
    from_dict: dict,
    keys: Sequence[Hashable],
    strict: bool,
    _initial_from_dict: dict,
    _initial_keys: Sequence[Hashable],
) -> Any | None:
    """Recursively extracts nested values from a dictionary."""
    if len(keys) == 0:
        return from_dict
    key = keys[0]
    if not strict:
        if isinstance(from_dict, dict):
            try:
                return _extract(
                    from_dict[key], keys[1:], strict, _initial_from_dict, _initial_keys
                )
            except (KeyError, TypeError):
                return None
    else:  # strict
        if isinstance(from_dict, dict):
            try:
                return _extract(
                    from_dict[key], keys[1:], strict, _initial_from_dict, _initial_keys
                )
            except KeyError:
                raise KeyNestedError(
                    f"Error traversing '{_initial_from_dict}' with keys '{_initial_keys}'. "
                    + (
                        f"There are no key '{key}' in nested '{from_dict}' element. "
                        if (from_dict, key) != (_initial_from_dict, _initial_keys)
                        else ""
                    )
                    + "Turn off 'strict' mode if you want to silence the exception"
                )
        else:
            raise ValueError(
                f"Error traversing '{_initial_from_dict}' with keys '{_initial_keys}'. "
                f"Non-dict value '{from_dict}' reached in nested dict, "
                f"while keys '{keys}' are still remained"
            )
    return None
