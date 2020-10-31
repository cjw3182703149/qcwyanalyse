import numpy

x = numpy.linspace(-5,5,50)
y = numpy.linspace(-5,5,50)
f = 2*x**2 + 3*x + 4*y**2 + 5
def J(x,y):
    return 2*x**2 + 3*x + 4*y**2 + 5
def dJX(x,y):
    return 8*y
def dJY(x,y):
    return 4 * x + 3
def dJX(x,y):
    return 8*y + 4*x + 3
eta = 0.1
epsilon = 0.1
x = 1
y = 1
while True:
    gradient = dJX(x,y)
    gradient2 = dJY(x,y)
    last_x = x
    last_y = y
    x = x - eta * gradient
    y = y - eta * gradient2
    if abs(J(x,y)-J(last_x,last_y)) < epsilon:
        break

print(J(x,y))
print(dJX(x))
