import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# For 10 cities simulation use no_of_iterations = 1000 and change no_of_cities = 10
# For 100 cities simulation use no_of_iterations = 100000 and change no_of_cities = 100

file = "100.txt" 
no_of_iterations = 65000
no_of_cities = 100
no_of_frames =800

locations = []
with open(file, "r") as points:
    loc = points.readlines()
    for i,ele  in enumerate(loc[1:]):
        x=float(ele.split()[0])
        y=float(ele.split()[1])
        locations.append([x,y, i])
locations.append(locations[0])


def total_distance(locations):
    sum = 0
    for i in range(len(locations)-1):
        sum += np.sqrt((locations[i][0]-locations[i+1][0])**2+(locations[i][1]-locations[i+1][1])**2)
    return sum

def cooling(temp, alpha):
    return temp*alpha


def check_accept(temp, current_solution, new_solution):
    prob = min(1, np.exp(-(new_solution - current_solution) / temp))
    if(prob > random.uniform(0,1)):
        return True
    else:
        return False
   
def best_route(cordinate, no_of_iterations,  Temp=1000, alpha=0.99):
    current_distance = total_distance(cordinate)
    best_distance = []
    best_distance.append(current_distance)
    Route = []
    Route.append(cordinate.copy())
    for _ in range(no_of_iterations):
        # Swap any two random location
        swap_list_indx = range( 1, len(cordinate)-1)
        i = random.randint(swap_list_indx[0], swap_list_indx[-1])
        j = random.randint(swap_list_indx[0], swap_list_indx[-1])
        if i == j:
            while i == j:
                j = random.randint(swap_list_indx[0], swap_list_indx[-1])
        new_order = cordinate.copy()
        new_order[min(i,j):max(j,i)+1] = reversed(new_order[min(i,j):max(j,i)+1])
        current_distance = total_distance(cordinate)
        new_distance = total_distance(new_order)
        if(new_distance<best_distance[-1]):
            best_distance.append(new_distance)
        else:
            best_distance.append(best_distance[-1])

        Temp = cooling(Temp, alpha)
        if(check_accept(Temp, current_distance, new_distance)):
            cordinate = new_order.copy()
        Route.append(cordinate.copy())
    return best_distance, Route

best_distance , best_path =   best_route(locations, no_of_iterations)

fig, ax = plt.subplots()
def onestep(frame):
    global best_distance
    ax.clear()
    distance = total_distance(best_path[frame])

    ax.set_title('Current Distance = '+str(np.round(distance, decimals=2))+'\n'
                 +"Best Distance = "+str(np.round(best_distance[frame], decimals=2))+
                '\n Iterations = '+str(frame) ) 
    ax.plot([best_path[frame][i][0] for i in range(no_of_cities+1)], [best_path[frame][i][1] for i in range(no_of_cities+1)])
    ax.plot([best_path[frame][i][0] for i in range(no_of_cities+1)], [best_path[frame][i][1] for i in range(no_of_cities+1)], 'ro')
ani= FuncAnimation(fig, onestep, frames=[(no_of_iterations//no_of_frames)*i for i in range(no_of_frames+1)], interval=100,repeat=False)
ani.save("100.gif")
plt.show()


