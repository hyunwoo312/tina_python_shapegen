import matplotlib.pyplot as plt
import numpy as np

# circle
circle = plt.Circle((0,0), 1, color='b', clip_on=False)
# figure
fig = plt.gcf()
ax = fig.gca()
ax.set_aspect('equal', adjustable='box')
plt.xlim(-2,2)
plt.ylim(-2,2)
# plot artist
ax.add_artist(circle)
ax.axis('off') # removes the axis to leave only the shape

fig.savefig('test.png')