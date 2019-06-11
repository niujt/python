def id(x):
    return x


def addc(x, y, k):
    return k(x + y)


def add_count(x):
    return lambda y: lambda k: k(x + y)


def addc_count(x, y):
    return lambda k: k(x + y)


if __name__ == '__main__':
    print(addc(1, 4, id))
    print(addc(1, 4, lambda x: addc(x, 2, id)))
    print(addc(1, 3, lambda x: addc(4, 5, lambda y: addc(x, y, id))))
    print(addc_count(2, 3)(addc_count(4, 5)(add_count))(id))
