def create_leaf(path: str, value):
    """
    Create a recursive dictionary according to the given path, and containing the leaf value.

    >>> create_leaf('a.b.c.d', 'Leaf value')
    >>> # {
    >>> #     'a': {
    >>> #         'b': {
    >>> #             'c': {
    >>> #                 'd': 'Leaf value'
    >>> #             }
    >>> #         }
    >>> #     }
    >>> # }
    """
    for comp in reversed(path.split('.')):
        value = {comp: value}

    return value
