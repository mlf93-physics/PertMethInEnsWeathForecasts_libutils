def product(*args, **kwds):
    """Calculates the product of all combinations of two iterators/lists/other

    Examples
    --------
    product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111

    Yields
    -------
    tuple
        The product of the next values in the iterators.
    """
    pools = list(map(tuple, args)) * kwds.get("repeat", 1)
    result = [[]]

    for pool in pools:
        result = [x + [y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)
