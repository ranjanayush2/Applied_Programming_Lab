import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def SA_optimization(func, starting_point, temperature, decay_rate, region):
    """
    region: it is range of values of x over which we want to find optimum value.
    """
    T = temperature
    decayrate = decay_rate
    bestcost = func(starting_point)
    # Generate several values within a search 'space' and check whether the new value is better
    # than the best seen so far.

    xbase = np.linspace(region[0], region[1], 100)
    ybase = func(xbase)
    fig, ax = plt.subplots()
    # ax.plot(xbase, ybase)
    bestx = starting_point
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'ro')
    lngood, = ax.plot([], [], 'go', markersize=10)
    def onestep(frame):
        ax.plot(xbase, ybase)
        nonlocal bestcost, bestx, decayrate, T
        # Generate a random value \in -2, +2
        dx = (np.random.random_sample() - 0.5) * T
        x = bestx + dx
        y = func(x)
        if y < bestcost:
            bestcost = y
            bestx = x
            lngood.set_data(x, y)
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(y-bestcost)/T):
                bestcost = y
                bestx = x
                lngood.set_data(x, y)
            pass
        T = T * decayrate
        xall.append(x)
        yall.append(y)
        lnall.set_data(xall, yall)
    ani= FuncAnimation(fig, onestep, frames=range(100), interval=100, repeat=False)
    plt.show()

def yfunc(x):
    return x**2 + np.sin(8*x)

SA_optimization(yfunc,-2, 3, 0.95,[-2,2] )

