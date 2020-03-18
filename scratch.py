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
    def __init__(self, x, speed):
        self.x = x
        self.y = 0.5
        self.speed = speed
        self.color = 'ro'
        self.scatter, = ax.plot(self.x, self.y, self.color)


    def move(self):
        # self.y += self.speed
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
        self.scatter, = ax.plot(self.x, self.y, 'bo')



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
    length = len(x_vals)

    for i in range(0, length-1):
        current_x = x_vals.pop(i)
        current_y = y_vals.pop(i)

        for t in x_vals:
            if current_x - 0.001 < t < current_x +0.001:
                people[i].colission()
                # next.append(people[i].scatter)
        
    return next


people = []
p1 = Person(0, 0.005)
p2 = Person(0.5, 0.0005)
people.append(p1)
people.append(p2)

ani = FuncAnimation(fig, func=next_frame, blit=False, interval=50)
plt.show()