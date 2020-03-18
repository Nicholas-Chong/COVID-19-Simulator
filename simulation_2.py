import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
from matplotlib.animation import FuncAnimation
from random import uniform

speed = 0.005
fig = plt.figure(figsize=(9,4))
ax = fig.add_subplot()
ax.set_xlim(right=2)
ax.set_ylim(top=1)

x_max = 2
y_max = 1
xy_min = 0

class Person:
    def __init__(self):
        self.x = uniform(0, 2)
        self.y = uniform(0, 1)
        self.speed = 0.005
        self.color = 'ro'
        self.scatter, = ax.plot(self.x, self.y, self.color)


    def move(self):
        self.y += self.speed
        self.x += self.speed

        # Right boundary
        if self.x >= x_max:
            self.speed = -self.speed
            self.x += self.speed
        
        # Top boundary
        if self.y >= y_max:
            self.speed = -self.speed
            self.y += self.speed

        # Bottom boundary
        if self.y <= xy_min:
            self.speed = -self.speed
            self.y += self.speed

        # Left boundary
        if self.x <= xy_min:
            self.speed = -self.speed
            self.x += self.speed

        self.scatter.set_xdata(self.x)
        self.scatter.set_ydata(self.y)


    def get_position(self):
        return [self.x, self.y]


    def colission(self):
        self.color = 'bo'


# def init():
#     frame = []
#     for i in people:
#         frame.append(i.scatter)

#     return frame


def next_frame(t):
    next = []
    for i in people:
        i.move()
        # next.append(i.scatter)
    
    new_positions = [i.get_position() for i in people]
    x_vals = [i.pop(0) for i in new_positions]
    y_vals = new_positions

    for i in range(0, len(x_vals)):
        for t in x_vals:
            if x_vals[i] - 0.001 < t < x_vals[i] +0.001:
                people[i].colission()
                # next.append(people[i].scatter)
        
    return next


people = []
for i in range(0, 100):
    person = Person()
    people.append(person)

ani = FuncAnimation(fig, func=next_frame, blit=True, interval=50)
plt.show()
