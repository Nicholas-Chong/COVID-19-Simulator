import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
from matplotlib.animation import FuncAnimation
from random import uniform, choice

speeds = [0.05, -0.05, 0.04, -0.04, 0.03, -0.03]

fig = plt.figure(figsize=(15,8))
ax = fig.add_subplot()

x_max = 10
y_max = 6
xy_min = 0

ax.set_xlim(right=x_max)
ax.set_ylim(top=y_max)

class Person:
    def __init__(self, num):
        self.key = num
        self.x = uniform(0, x_max)
        self.y = uniform(0, y_max)
        self.x_speed = choice(speeds)
        self.y_speed = choice(speeds)
        self.color = 'ro'
        self.multiplier = 1


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


    def get_position(self):
        return [round(self.x, 3), round(self.y, 3)]


    def colission(self):
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

            if x_diff_before <= 0.005:
                y_before = positions[i-1][1][1]
                y_current = positions[i][1][1]
                y_diff_before = y_current - y_before
                if y_diff_before <= 0.005:
                    people[positions[i-1][0]].colission()
                    people[positions[i][0]].colission()
                    
                    people[positions[i-1][0]].intermittent_draw()
                    people[positions[i][0]].intermittent_draw()
            else:
                people[positions[i][0]].intermittent_draw()
        else:
            people[positions[i][0]].intermittent_draw()


people = []
for i in range(0, 100):
    person = Person(i)
    person.init_draw()
    people.append(person)

ani = FuncAnimation(fig, func=next_frame, blit=False, interval=50)
plt.show()
