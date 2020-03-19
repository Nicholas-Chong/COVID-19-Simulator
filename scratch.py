import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
from matplotlib.animation import FuncAnimation
from random import uniform

speed = 0.005
fig = plt.figure(figsize=(9,4))
ax = fig.add_subplot()
ax.set_xlim(right=4)
ax.set_ylim(top=2)

x_max = 4
y_max = 2
xy_min = 0

class Person:
    def __init__(self, num):
        self.key = num
        self.x = uniform(0, 4)
        self.y = uniform(0, 2)
        self.speed = 0.005
        self.color = 'ro'


    def init_draw(self):
        self.scatter, = ax.plot(self.x, self.y, self.color)


    def intermittent_draw(self):
        self.scatter.set_xdata(self.x)
        self.scatter.set_ydata(self.y)


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


    def get_position(self):
        return [round(self.x, 3), round(self.y, 3)]


    def colission(self):
        self.scatter.set_color('b')
        self.speed = -self.speed


def init():
    return []


def next_frame(t):
    for i in people:
        i.move()
    
    # COLLISION DETECTION
    # new_positions = [i.get_position() for i in people]
    positions = []
    for i in people:
        data = [i.key, i.get_position()]
        positions.append(data)

    positions.sort(key=lambda x: x[1])
    
    for i in range(0, len(positions)-1):
        if i > 0:
            x_before = positions[i-1][1][0]
            x_current = positions[i][1][0]
            x_diff_before = x_current - x_before

            if x_diff_before <= 0.01:
                y_before = positions[i-1][1][1]
                y_current = positions[i][1][1]
                y_diff_before = y_current - y_before
                if y_diff_before <= 0.01:
                    people[positions[i-1][0]].colission()
                    people[positions[i][0]].colission()
                    
                    people[positions[i-1][0]].intermittent_draw()
                    people[positions[i][0]].intermittent_draw()
            else:
                people[positions[i][0]].intermittent_draw()
        else:
            people[positions[i][0]].intermittent_draw()


people = []
for i in range(0, 25):
    person = Person(i)
    person.init_draw()
    people.append(person)

ani = FuncAnimation(fig, func=next_frame, blit=False, interval=25)
plt.show()
