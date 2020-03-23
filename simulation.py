#------------------------------------------------------------------------------
# Name:       simulation.py
# Purpose:    To visualize the spread of a virus during a pandemic 
#             with/without social distancing
#
# Author:      Nicholas Chong
# Created:     15-Mar-2020
#------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as ax
from matplotlib.animation import FuncAnimation
from random import uniform, choice

speeds = [
    0.08, -0.08, 
    0.07, -0.07, 
    0.06, -0.06, 
    0.05, -0.05, 
    0.04, -0.04, 
    0, 0
    ]

# ---------------------------CREATE FIGURES/PLOTS------------------------------

# Create upper graph
fig = plt.figure(figsize=(10,8))
ax = plt.subplot(211) # (rows, columns, plot index)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
plt.title('Free For All')

x_max = 10
y_max = 6
xy_min = 0

ax.set_xlim(right=x_max)
ax.set_ylim(top=y_max)

# Create bottom graph
ax2 = plt.subplot(212)
ax2.set_xlim(right=1000)
ax2.set_ylim(top=70)
plt.ylabel('# of People Infected')
plt.xlabel('Time')

# ----------------------CLASS AND FUNCTION DEFINITION--------------------------

class Person:
    def __init__(self, num, is_isolating):
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
        
        self.is_isolating = is_isolating


    def init_draw(self):
        self.scatter, = ax.plot(self.x, self.y, self.color)


    def intermittent_draw(self):
        self.scatter.set_xdata(self.x)
        self.scatter.set_ydata(self.y)


    def move(self):
        if self.is_isolating == False:
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
        if self.x_speed < 0:
            self.x_speed = abs(choice(speeds))
            self.y_speed = abs(choice(speeds))
        else:
            self.x_speed = -1 * abs(choice(speeds))
            self.y_speed = -1 * abs(choice(speeds))

    
    def infect(self):
        if self.has_been_infected == False:
            self.infected = True
            self.has_been_infected = True

        self.scatter.set_color('b')


def next_frame(t):

    infected = 0

    # First graph (moving dots)

    for i in people:
        if i.infected == True:
            infected += 1

        i.move()
    
    # COLLISION DETECTION
    positions = [] # [[person key, [x, y]], [person key, [x, y]]...]
    for i in people:
        # i.key will return the same value as the person-object's location in 
        # the people list
        data = [i.key, i.get_position()] 
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

                    if people[positions[i-1][0]].infected == True:
                        people[positions[i][0]].infect()

                    if people[positions[i][0]].infected == True:
                        people[positions[i-1][0]].infect()
                    
                    # Call draw methods to update position
                    people[positions[i-1][0]].intermittent_draw()
                    people[positions[i][0]].intermittent_draw()

            else:
                people[positions[i][0]].intermittent_draw()

        else:
            people[positions[i][0]].intermittent_draw()

    ax2.plot(t, infected, 'r.')
    
    if t == 1000:
        ani.event_source.stop()


def setup():
    title = input('Name this simulation: ')
    social_distancing = input('Social Distancing? Y/N: ')

    if social_distancing == 'Y':
        social_distancing = True

    else:
        social_distancing = False
    
    if social_distancing == True:
        social_distancing_level = input('Social Distancing Level HIGH/MED: ')

        if social_distancing_level == 'HIGH':
            social_distancing_level = 2

        else:
            social_distancing_level = 4
            
    else:
        social_distancing_level = None

    dict = {}
    dict['title'] = title
    dict['sd'] = social_distancing
    dict['sdl'] = social_distancing_level
    
    return dict


# --------------------------------MAIN CODE------------------------------------

settings = setup()

title = settings['title']
social_distancing = settings['sd']
social_distancing_lvl = settings['sdl']

plt.subplot(211)
plt.title(title)

people = [] # people is a global variable
for i in range(0, 100):
    if social_distancing == True:
        if i % social_distancing_lvl == 0:
            bool = True
        else:
            bool = False

    else:
        bool = False

    person = Person(i, bool)
    person.init_draw()
    people.append(person)

# Randomly choose 2 people to start off with the infection
choice(people).infect()
choice(people).infect()

# Create animation
ani = FuncAnimation(fig, func=next_frame, interval=10)
plt.show()