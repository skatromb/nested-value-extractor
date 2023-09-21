```python
>>> extract_nested_value({1: {2: {3: "value"}}}, [1, 2, 3])
"value
```

Extracts a nested value from a JSON-like dict by specifying a sequence of keys.

May be useful to avoid a `KeyError` exception when accessing JSON-like dicts with a dynamic nested structure,
when you know the key paths of elements, but are unsure whether elements exist.

Returns the nested value or `None` if it wasn't found. Could throw a `KeyError` exception if `strict=True` is passed.


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
KeyError: "Keys sequence '["a"]' do not exists in object '{1: 2}'")
```

### Arguments
- `from_obj`: JSON-like dict from which the nested value should be extracted
- `keys`: ordered sequence of keys to derive the nested value
- `strict`: (default False) prevents throwing an exception when keys are not exist in nested object when set to False.
  Throws KeyError exception if set to True and key wasn't found.


### Returns
Nested value, if the entire chain of keys is present, or None

### Development
Look at [Makefile](./Makefile)
