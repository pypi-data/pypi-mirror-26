Complex certifier types:
========================

All complex certifiers can take other certifiers as arguments.

certify_set:
------------

    >>> from certifiable import certify_set
    >>> certify_set(set())
    >>> certify_set(set([1,2,3]))
    >>> certify_set(list([1,2,3]))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/complex.py", line 58, in certify_set
        required=required,
    CertifierTypeError: expected "set", got 'list'

    >>> value = set()
    >>> certify_set(set([1,2,3]), certifier=certify_int(min_value=1, max_value=10)
    >>> certify_set(set(['hello']), certifier=certify_int(min_value=1, max_value=10))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/complex.py", line 79, in certify_set
        certifier(item)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 213, in certify_int
        required=required,
    CertifierTypeError: expected integer, but value is of type 'str'


certify_tuple:
--------------

    >>> from certifiable import certify_tuple
    >>> certify_tuple(tuple())
    >>> certify_tuple((1, ))
    >>> certify_tuple(list([1,2,3]))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 211, in certify_tuple
        required=required,
    CertifierTypeError: value is not a tuple ('list')

An optional schema allows for fine-grained control of the tuple's items:

    >>> certifier = certify_tuple(schema=(
    ...     certify_string(min_length=2),
    ...     certify_int(min=10),
    ...     ))
    >>> value = ('hello', 12)
    >>> certifier(value)

    >>> value = ('hello', 12, 'bang')
    >>> certifier(value)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 220, in certify_tuple
        required=required,
    CertifierValueError: encountered 1 extra items

    >>> value = ('hello', 'world')
    >>> certifier(value)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 234, in certify_tuple
        exc,
    CertifierValueError: invalid value 'world' for item 1


certify_dict:
-------------

    >>> from certifiable import certify_dict
    >>> certify_dict(dict())
    >>> certify_dict({'hello': 'world'})
    >>> certify_dict(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 128, in certify_dict
        required=required,
    CertifierTypeError: Expected dictionary but the type is 'int'

Optional `schema`, `key_certifier` or `value_certifier` fuctions allows for fine-grained control
of the dicts's items - any combination can be used together:

    >>> value = {'hello': 'world'}
    >>> certifier = certify_dict(schema={
    ...    'id': certify_string,
    ...    'count': certify_int(min=0),
    ...    })
    >>> certifier({'id': 'hello', 'count': 123})

    >>> certifier({'key': 'hello'})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 141, in certify_dict
        required=required,
    CertifierValueError: key count missing from dictionary {}

    >>> certifier({'key': 'hello', 'count': 'world'})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 158, in certify_dict
        exc,
    CertifierValueError: invalid value 'world' for key 'count'

    >>> certifier = certify_dict(key_certifier=certify_string)
    >>> certifier({'id': 'hello', 'count': 123})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 134, in certify_dict
        key_certifier(key)
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 159, in certify_string
        required=required,
    CertifierTypeError: expected string, but value is of type 'int'

    >>> certifier = certify_dict(value_certifier=certify_string)
    >>> certifier({'id': 'hello', 'count': 123})
    >>> certifier({'id': 'hello', 123:  'world'})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 137, in certify_dict
        value_certifier(key)
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 159, in certify_string
        required=required,
    CertifierTypeError: expected string, but value is of type 'int'


certify_list:
-------------

    >>> from certifiable import certify_list
    >>> certify_list(list())
    >>> certify_list([1,2,3])
    >>> certify_list(tuple())
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 268, in certify_list
        required=required,
    CertifierTypeError: expected "list", got 'tuple'

An optional `certifier` function allows for fine-grained control of the list's items:

    >>> certifier = certify_list([1,2,3], certifier=certify_int(min_value=1, max_value=10))
    >>> certifier = certify_list([1,20,3], certifier=certify_int(min_value=1, max_value=10))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 289, in certify_list
        certifier(item)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 229, in certify_int
        required=required,
    CertifierValueError: 20 is more than minimum acceptable 10

    >>> certifier = certify_list(['hello'], certifier=certify_int(min_value=1, max_value=10))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 289, in certify_list
        certifier(item)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 213, in certify_int
        required=required,
    CertifierTypeError: expected integer, but value is of type 'str'



certify_json:
-------------

T.B.D.


certify_email:
--------------

T.B.D.

