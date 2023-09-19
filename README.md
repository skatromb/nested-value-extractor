```python
>>> extract_nested_value({1: {2: {3: "value"}}}, [1, 2, 3])
"value"
```

Derives a nested value from dict by specifying a sequence of keys.

Could be useful to avoid `KeyError` exception when parsing JSONs with dynamic structure,
when you know JSON paths of elements, but unsure if the element exists.

Returns nested value or `None` if it wasn't found. If you want to enforce throwing exceptions, pass `strict=True`.



### Examples
```python
>>> extract_nested_value({1: 2}, [1])
2

>>> extract_nested_value({1: {2: {3: "value"}}}, [1, 2, 3])
"value"

>>> extract_nested_value({1: 2}, ["a"])
None

>>> extract_nested_value({1: 2}, [])
{1: 2}

>>> extract_nested_value({1: 2}, ["a"], strict=True)
raise KeyNestedError("Error traversing '{1: 2}' with keys '['a']'.
There are no key 'a' in nested '{1: 2}' element.
Turn off 'strict' mode if you want to silence the exception")
```

### Arguments
- `from_dict`: dict from which the nested value is extracted
- `keys`: ordered sequence of keys to derive the nested value
- `strict`: prevents throwing an exception when keys are not exist in nested dict if True

### Returns
Nested value if all chain of keys exists, or `None`

### Development
Look at [Makefile](./Makefile)
