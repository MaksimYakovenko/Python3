import numpy as np
from matplotlib import pyplot as plt


NUM = 500


def fun(x):
    try:
        y = 1 / (1 + x ** 2)
    except Exception as e:
        print('Exception handling', e)
        n = x.size
        y = np.zeros(n)
        for i in range(n):
            y[i] = 1 / (1 + x[i] ** 2)
    return y


def taylor_fun(n):
    def _taylor_fun(x):
        s = np.zeros(x.size)
        a = 1
        for k in range(1, n, 2):
            s += a
            a *= - x * x
        return s
    _taylor_fun.__name__ = f"taylor(fun, {n})"
    return _taylor_fun


def lagrange(f, a, b, n):
    xk = np.linspace(a, b, n)
    yk = f(xk)

    def _lagrange(x):
        y = np.zeros_like(x)
        lk = np.ones_like(x)
        for k in range(n):
            lk.fill(1)
            for i in range(n):
                if i != k:
                    lk *= (x - xk[i]) / (xk[k] - xk[i])
            y += yk[k] * lk
        return y

    _lagrange.__name__ = f"lagrange({f.__name__}, {n})"
    return _lagrange


def linear_interpolation(f, a, b, k):
    xk = np.linspace(a, b, k)
    yk = f(xk)

    def _linear_interpolation(x):
        y = np.interp(x, xk, yk)
        return y

    _linear_interpolation.__name__ = f"linear_interpolation({f.__name__},{k})"
    return _linear_interpolation


def average_error(f1, f2, xmin, xmax, ymin, ymax):
    box_square = (xmax - xmin) * (ymax - ymin)
    count = int(box_square) * NUM
    x = np.random.uniform(xmin, xmax, count)
    y = np.random.uniform(ymin, ymax, count)
    y1 = f1(x)
    y2 = f2(x)
    count_in = np.sum(
        np.logical_or(
            np.logical_and(y1 <= y, y <= y2),
            np.logical_and(y2 <= y, y <= y1)
        )
    )
    # print(count, count_in)
    square = box_square * count_in / count
    # print(square, box_square)
    return np.sqrt(square / box_square)


def move_axes():
    a0, b0, c0, d0 = plt.axis()
    d0 = (b0 - a0) * 3 / 3
    c0 = - d0
    plt.axis([a0, b0, c0, d0])
    ax = plt.gca()
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["left"].set_position(("data", 0))
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    # Підписуємо графіки
    plt.legend(loc="best")


def plot_f1f2(x, f1, f2):
    y1 = f1(x)
    y2 = f2(x)
    plt.plot(x, y1, "-b", lw=2, label=f1.__name__)
    plt.plot(x, y2, "-r", lw=2, label=f2.__name__)
    plt.fill_between(x, y1, y2, facecolor="yellow")

    error = average_error(f1, f2, *plt.axis())
    print(f"Середня похибка наближення для {f2.__name__}: {error}")

    move_axes()


def plot_diff(x, f1, f2):
    y = f2(x) - f1(x)
    plt.plot(x, y, "-m", label="difference")
    plt.fill_between(x, y, facecolor="pink")

    move_axes()


def plot_functions(a, b, interpolated, *interpolators):
    plt.figure(figsize=((b - a) / 2 * len(interpolators), 3 / 4 * (b - a)))
    x = np.linspace(a, b, int(b - a) * 50)

    for i in range(len(interpolators)):
        plt.subplot(2, len(interpolators), i + 1)
        plot_f1f2(x, interpolated, interpolators[i])
        plt.subplot(2, len(interpolators), i + 1 + len(interpolators))
        plot_diff(x, interpolated, interpolators[i])
    plt.show()


if __name__ == "__main__":
    a = -3
    b = 2.5
    m = 10
    n = 7
    k = 7
    plot_functions(
        a, b,
        fun,
        taylor_fun(m),
        lagrange(fun, a, b, n),
        linear_interpolation(fun, a, b, k)
    )

