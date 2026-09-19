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

        fun=f(a+h,b,c)
        print("a nudged by h:",fun)
        fun1=f(a,b+h,c)
        print("b nudged by h:",fun1)
        fun2=f(a,b,c+h)
        print("c nudged by h:",fun2)

        slope=(f(a+h,b,c)-f(a,b,c))/h
        print("a nudged by h:",slope)
        slope1=(f(a,b+h,c)-f(a,b,c))/h
        print("b nudged by h:",slope1)
        slope2=(f(a,b,c+h)-f(a,b,c))/h
        print("c nudged by h:",slope2)

    # day2()

    def day3():
        a=2.0
        b=-3.0
        c=10.0
        k=-2.0
        h=1e-5

        # forward
        e = a*b
        d = e+c
        L = d*k
        print("forward: e =",e,"d =",d,"L =",L)

        # the graph, entered at three different points
        def from_inputs(a,b,c,k):
            return ((a*b)+c)*k

        def from_e(e,c,k):
            return (e+c)*k

        def from_d(d,k):
            return d*k

        base = from_inputs(a,b,c,k)

        dL_dL = ((L+h)-L)/h
        dL_dd = (from_d(d+h,k)-base)/h
        dL_de = (from_e(e+h,c,k)-base)/h
        dL_dc = (from_inputs(a,b,c+h,k)-base)/h
        dL_da = (from_inputs(a+h,b,c,k)-base)/h
        dL_db = (from_inputs(a,b+h,c,k)-base)/h
        dL_dk = (from_inputs(a,b,c,k+h)-base)/h

        print("dL/dL =",dL_dL)
        print("dL/dd =",dL_dd)
        print("dL/de =",dL_de)
        print("dL/dc =",dL_dc)
        print("dL/da =",dL_da)
        print("dL/db =",dL_db)
        print("dL/dk =",dL_dk)

    day3()
