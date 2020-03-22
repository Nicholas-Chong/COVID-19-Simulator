import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
from matplotlib.animation import FuncAnimation
from random import uniform, choice

speeds = [0.05, -0.05, 0.04, -0.04, 0.03, -0.03, 0.02, -0.02, 0.01, -0.01]

# Create figure/plot/axes
fig = plt.figure(figsize=(10,8))
ax = plt.subplot(211) # (rows, columns, plot index)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

x_max = 10
y_max = 6
xy_min = 0

ax.set_xlim(right=x_max)
ax.set_ylim(top=y_max)

# Create bottom graph
ax2 = plt.subplot(212)
ax2.set_xlim(right=750)
ax2.set_ylim(top=100)

class Person:
    def __init__(self, num):
        self.key = num
        self.x = uniform(0, x_max)
        self.y = uniform(0, y_max)
        self.x_speed = choice(speeds)
        self.y_speed = choice(speeds)
        self.color = 'ro'
        self.multiplier = 1

        self.infected = False
        self.has_been_infected = False
        self.time_infected = -1


    def init_draw(self):
        self.scatter, = ax.plot(self.x, self.y, self.color)


    def intermittent_draw(self):
        self.scatter.set_xdata(self.x)
        self.scatter.set_ydata(self.y)


    def move(self):
        self.y += self.x_speed
        self.x += self.y_speed

        if self.x >= x_max or self.x <= xy_min or self.y >= y_max or self.y <= xy_min:
            self.x_speed = -self.x_speed
            self.y_speed = -self.y_speed

        if self.infected == True:
            self.time_infected += 1

        if self.time_infected == 200:
            self.infected = False
            self.scatter.set_color('g')


    def get_position(self):
        return [round(self.x, 3), round(self.y, 3)]


    def colission(self):
        if self.has_been_infected == False:
            self.infected = True
            self.has_been_infected = True

        self.scatter.set_color('b')
        if self.x_speed < 0:
            self.x_speed = abs(choice(speeds))
            self.y_speed = abs(choice(speeds))
        else:
            self.x_speed = -1 * abs(choice(speeds))
            self.y_speed = -1 * abs(choice(speeds))


def init():
    return []


def next_frame(t):

    infected = 0

    # First graph (moving dots)

    next = []
    for i in people:
        if i.infected == True:
            infected += 1

        i.move()
    
    # COLLISION DETECTION
    positions = [] # [[person key, [x, y]], [person key, [x, y]]...]
    for i in people:
        data = [i.key, i.get_position()] # i.key will return the same value as the person-object's location in the people list
        positions.append(data)

    positions.sort(key=lambda x: x[1]) # Sort list by x values
    
    for i in range(0, len(positions)-1):
        if i > 0:
            # Compare the distance between two x vals
            x_before = positions[i-1][1][0]
            x_current = positions[i][1][0]
            x_diff_before = x_current - x_before

            if x_diff_before <= 0.09: # -> threshold for contact
                # Compare the distance between two y vals
                y_before = positions[i-1][1][1]
                y_current = positions[i][1][1]

                if y_current > y_before:
                    y_diff_before = y_current - y_before
                
                else:
                    y_diff_before = y_before - y_current

                if y_diff_before <= 0.09: # -> threshold for contact
                    # Call collision methods
                    people[positions[i-1][0]].colission()
                    people[positions[i][0]].colission()
                    
                    # Call draw methods to update position
                    people[positions[i-1][0]].intermittent_draw()
                    people[positions[i][0]].intermittent_draw()



            else:
                people[positions[i][0]].intermittent_draw()

        else:
            people[positions[i][0]].intermittent_draw()

    ax2.plot(t, infected, 'r.')

culmulative_infected = []
people = [] # people is a global variable
for i in range(0, 75):
    person = Person(i) # Set the key value equal to it's position in the list
    person.init_draw()
    people.append(person)

# Create animation
ani = FuncAnimation(fig, func=next_frame, init_func=init, 
    interval=10)
plt.show()