def f(x):
    return 3*x**2 - 4*x + 5

def f(a,b,c):
    return a*b + c


if __name__ == "__main__":

    def day1():
        x=2.0
        for h in [1e-1,1e-3,1e-6,1e-10,1e-15]:
            slope = (f(x+h)-f(x))/h
            print(h,slope)

    # day1()

    def day2():
        a=2.0
        b=-3.0
        c=10.0
        h = 1e-5

        slope=f(a+h,b,c)
        print("a nudged by h:",slope)
        slope2=f(a,b+h,c)
        print("b nudged by h:",slope2)
        slope3=f(a,b,c+h)
        print("c nudged by h:",slope3)

    day2()
