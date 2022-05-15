import matplotlib.pyplot as plt
import numpy as np

# Funkcja zadana
def f(x):
    #return 1.5*x**4 - 2.2*x**3 - 3.1*x**2 + 1.8*x + 2.8
    return x**2

# Pochodna funkcji zadanej
def df(x):
    return 2*x
    #return 6*x**3 - 6.6*x**2 - 6.2*x + 1.8

# Metoda gradientu prostego
def simple_gradient_descent():
    ### PARAMETRY ###
    # maksymalna liczba iteracji
    i_max = 50 
    # obszar rysowania funkcji
    range_min = -1.7
    range_max = 2.4
    # x początkowy
    start = -3
    # współczynnik uczenia
    beta = 0.1
    # dokładność algorytmu
    err = 0.0001

    ### LOGIKA ###
    point = start
    points = np.array(start)
    i = 0
    while(True):
        i += 1
        last_point = point
        point = last_point - beta*df(last_point) # obliczanie nowego punktu
        points = np.append(points, point)
        # Warunek znalezienia minimum
        if abs(point - last_point) <= err: 
            print("Liczba iteracji: " + str(i))
            break
        # Przekroczenie maksymalnej liczby iteracji
        if i >= i_max:
            print("Nie znaleziono")
            break

    ### PREZENTACJA ###
    x_axis = np.linspace(range_min, range_max, 1000)
    plt.plot(x_axis, f(x_axis), 'b', linewidth = 1.0)
    plt.plot(points, f(points), 'r-o', linewidth = 2.0)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.suptitle("skok: " + str(beta) + "   x początkowe: " + str(start))
    plt.show()

simple_gradient_descent()
