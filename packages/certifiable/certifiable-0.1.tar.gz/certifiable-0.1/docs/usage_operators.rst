Certifiable operators
=====================

Use operators to perform logical groupings of core, advanced or operator certifiers.

Certifiers accept any callable, but one which should receive `value` when required to certify.
Using make_certifier is a great way to create and bake-in certification params.

XOR / certify_only_one:
-----------------------

Only one of the certifiers should be successful, if not then the first exception is re-raised.

    >>> from certifiable import XOR, certify_list, certify_string
    >>> value = 123
    >>> XOR(lambda: certify_int(value), lambda: certify_string(min_length=1))

    >>> value = float(2.3)
    >>> XOR(lambda: certify_list(value), lambda: certify_string(value))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/operators.py", line 86, in XOR
        raise exc
    CertifierValueError: Expected at least one certified value

ANY / certify_any:
------------------

Any of the certifiers `can` be successful (all exceptions are silently swallowed).

    >>> from certifiable import ANY, certify_list, certify_string
    >>> value = 123
    >>> ANY(lambda: certify_int(value), lambda: certify_string(value))
    >>> ANY(lambda: certify_list(value), lambda: certify_string(value))


AND / certify_all:
------------------

All of the certifiers should be successful, if not then the first exception is re-raised.

    >>> from certifiable import XOR, certify_list, certify_int
    >>> value = 123
    >>> AND(lambda: certify_list([value]), lambda: certify_int(value))

    >>> AND(lambda: certify_list(value), lambda: certify_int(value))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/operators.py", line 40, in AND
        arg()
      File "<stdin>", line 1, in <lambda>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/complex.py", line 268, in certify_list
        required=required,
    CertifierTypeError: expected "list", got 'int'


NAND / certify_none:
--------------------

All of the certifiers should fail, if not then the first exception is re-raised.

    >>> from certifiable import XOR, certify_list, certify_int
    >>> value = 123
    >>> NAND(lambda: certify_list(value), lambda: certify_string(value))
    >>> NAND(lambda: certify_list(value), lambda: certify_int(value))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/operators.py", line 66, in NAND
        raise exc
    CertifierValueError: Expecting no certified values
