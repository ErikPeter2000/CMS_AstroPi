# def sequence_value(n):
#     return 5 * (-2)**(n - 1)

# target_value = 100**100
# n = 1

# while sequence_value(n) <= target_value:
#     n += 1
# # print(sequence_value(n))
# print(sequence_value(661)-target_value)

# print("The smallest value of n where u_n > 100^100 is:", n)


import math


def f(x):
  return ((1+x**2))**12

def trapezoidal(f, a, b, n):
    h = float(b - a) / n
    s = 0.0
    s += f(a)/2.0
    for i in range(1, n):
        s += f(a + i*h)
        # print(s*h)
    s += f(b)/2.0
    return s * h


def trapezium2(f,a,b,n):
   return (0.5*(f(a)+f(b) +(2*sum([f(ele) for ele in range(a*n,(b)*n,(1))]))))/(n*n)

resolution = 5
bound1 = 0
bound2 = 0.5
# (bound2-bound1)/resolution 
print(trapezoidal(f, bound1, bound2, resolution))
# print(trapezium2(f, bound1, bound2, resolution))