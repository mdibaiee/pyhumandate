humandate
---------

Parse human-readable dates in Python in arbitrary strings.

Usage
-----

Install using `pip`:

```
pip install humandate

```

Use the `parse_date` function:

```python
from humandate import parse_date

print(parse_date('next month'))
print(parse_date('I was there an hour ago!'))
print(parse_date('Our event will be held at 12 tomorrow!'))
```

For more examples see [tests.py](humandate/tests.py)
