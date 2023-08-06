Certifier `required` parameter:
===============================

When no value is provided but one is expected (`required` always defaults to True):

    >>> from certifiable import certify_int
    >>> certify_int(None, required=False)
    >>> certify_int(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "certifiable/utils.py", line 36, in wrapper
        certify(value)
      File "certifiable/utils.py", line 33, in certify
        func(val, **kwargs)
      File "certifiable/core.py", line 204, in certify_int
        required=required,
      File "certifiable/utils.py", line 49, in certify_required
        message="required value is None",
    CertifierTypeError: required value is None


