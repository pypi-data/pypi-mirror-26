Core certifiers
===============

Examples of certifying type...

certify_bool:
-------------

    >>> from certifiable import certify_bool
    >>> certify_bool(True)
    >>> certify_bool(False)
    >>> certify_bool(1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 302, in certify_bool
        required=required,
    CertifierTypeError: expected bool, but value is of type 'int'


certify_int:
------------

    >>> from certifiable import certify_int
    >>> certify_int(-100)
    >>> certify_int(0)
    >>> certify_int(123L)
    >>> certify_int('bang')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 212, in certify_int
        required=required,
    CertifierTypeError: expected integer, but value is of type 'str'


certify_number:
---------------

    >>> from certifiable import certify_number
    >>> import Decimal
    >>> certify_number(-100)                # integer
    >>> certify_number(0)
    >>> certify_number(123L)                # long
    >>> certify_number(1.234)               # float
    >>> certify_number(0xdeadbeef)          # hex
    >>> certify_number(05)                  # octal
    >>> certify_number(Decimal(456))        # Decimal
    >>> certify_number('bang')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 212, in certify_int
        required=required,
    CertifierTypeError: expected integer, but value is of type 'str'


certify_bytes:
--------------

    >>> from certifiable import certify_bytes
    >>> certify_bytes('hello world')
    >>> certify_bytes(b'hello world')
    >>> certify_bytes(u'hello world')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 337, in certify_bytes
        required=required,
    CertifierTypeError: expected byte string, but value is of type 'unicode'


certify_enum:
-------------

    >>> from certifiable import certify_enum
    >>> from enum import Enum
    >>> hello(Enum):
    ...     world = 1
    >>> certify_enum(hello.world)


certify_enum_value:
-------------------

    >>> from certifiable import certify_enum_value
    >>> from enum import Enum
    >>> hello(Enum):
    ...     world = 1
    >>> certify_enum_value(hello.world)
    >>> certify_enum_value(1)
    >>> certify_enum_value(2)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 420, in certify_enum_value
        required=required,
    certifiable.errors.CertifierValueError: value 2 is not a valid member of 'hello'


certify_text:
-------------

    >>> from certifiable import certify_text
    >>> certify_text(u'\u0008', nonprintable=True)
    >>> certify_text(u'\u0008', nonprintable=False)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 122, in certify_text
        required=required,
      File "certifiable/core.py", line 34, in _certify_printable
        required=required,
    certifiable.errors.CertifierValueError: string contains non-printable characters


certify_string:
---------------

    >>> from certifiable import certify_string
    >>> certify_string(u'hello')
    >>> certify_string('world')
    >>> certify_string(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 159, in certify_string
        required=required,
    CertifierTypeError: expected string, but value is of type 'int'


certify_timestamp:
------------------
    >>> from certifiable import certify_timestamp
    >>> from datetime import datetime
    >>> certify_timestamp(datetime.utcnow())
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 486, in certify_date
        required=required,
    CertifierTypeError: expected timestamp (datetime), but value is of type 'int'


certify_date:
-------------
    >>> from certifiable import certify_date
    >>> from datetime import date
    >>> certify_date(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 538, in certify_date
        required=required,
    CertifierTypeError: expected timestamp (date), but value is of type 'int'


certify_time:
-------------
    >>> from certifiable import certify_time
    >>> from datetime import time
    >>> certify_time(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 512, in certify_time
        required=required,
    CertifierTypeError: expected timestamp (time), but value is of type 'int'


certify_object:
---------------
    >>> from certifiable import certify_object
    >>> certify_object('hello', kind=six.string_types)
    >>> certify_object('world', kind=unicode)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 458, in certify_object
        required=required,
    CertifierValueError: Expected object <type 'unicode'>, but got 'str'
