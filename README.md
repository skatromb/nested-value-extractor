# nested-dict-extractor
Derives nested value from dict by providing sequence of keys. 

Returns `None` if nested value wasn't found or throws an Exception if `strict=True`

```python
>>> extract_nested_value({1: {2: {3: "value"}}}, [1, 2, 3])
"value"
```

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

```

### Arguments
`from_dict`: dict from which the nested value is extracted
`keys`: ordered sequence of keys to derive the nested value
`strict`: prevents throwing an exception when keys are not exist in nested dict if True

### Returns
Nested value if all keys are exists, or None

### Development
Look at [Makefile](./Makefile)