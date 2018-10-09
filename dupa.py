# transformacja na nowe wspolrzedne
def y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return (((y - y_a) * (x_c - x_a)) - ((y_c - y_a) * (x + x_a))) / (
            ((y_b - y_a) * (x_c - x_a)) + ((y_c - y_a) * (x_a - x_b)))


def x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return ((x - x_a - (x_b * y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c))) / (x_c - x_a)) + (
            x_a * (((y - y_a) * (x_c - x_a)) - ((y_c - y_a) * (x - x_a))) / (
            (x_c - x_a) * (((y_b - y_a) * (x_c - x_a)) + ((y_c - y_a) * (x_a - x_b)))))


# z nowych na stare
def x(y_nowe, y_a, y_b, y_c, x_nowe, x_a, x_b, x_c):
    return (x_c - x_a) * x_nowe + (x_b - x_a) * y_nowe + x_a


def y(y_nowe, y_a, y_b, y_c, x_nowe, x_a, x_b, x_c):
    return (y_c - y_a) * x_nowe + (y_b - y_a) * y_nowe + y_a


# Psi
def psi1(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return 1 - x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c) - y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c)


def psi2(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c)


def psi3(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c)


def psi4(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return 4 * y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c) * (
            1 - x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c) - y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c))


def psi5(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return 4 * x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c) * (
            1 - x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c) - y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c))


def psi6(y, y_a, y_b, y_c, x, x_a, x_b, x_c):
    return 4 * x_(y, y_a, y_b, y_c, x, x_a, x_b, x_c) * y_(y, y_a, y_b, y_c, x, x_a, x_b, x_c)


# pochodne
if __name__ == '__main__':
    x_a = 10
    y_a = 10

    x_b = 10
    y_b = 20

    x_c = 1100
    y_c = 10

    x_stare = 10.5
    y_stare = 10.3

    x_nowe = x_(y_stare, y_a, y_b, y_c, x_stare, x_a, x_b, x_c)
    y_nowe = y_(y_stare, y_a, y_b, y_c, x_stare, x_a, x_b, x_c)
    print x_nowe, y_nowe

    x_stare2 = x(y_nowe, y_a, y_b, y_c, x_nowe, x_a, x_b, x_c)
    y_stare2 = y(y_nowe, y_a, y_b, y_c, x_nowe, x_a, x_b, x_c)
    print x_stare2, y_stare2
