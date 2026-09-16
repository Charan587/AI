def f(x):
    return 3*x**2 - 4*x + 5


if __name__ == "__main__":
    x=2.0
    for h in [1e-1,1e-3,1e-6,1e-10,1e-15]:
        slope = (f(x+h)-f(x))/h
        print(h,slope)