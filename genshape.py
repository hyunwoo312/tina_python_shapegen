from matplotlib.path import Path
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from skimage import color as skolor
from skimage import measure
from scipy.ndimage import gaussian_filter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product, combinations
import os
from datetime import datetime
import params as ps
LIST = ['circle', 'ellipse', 'contour', 'sphere', 'cube']

def generate(shape = 'sample', **params):
    # sample. . .
    if shape == 'sample':
        return circle()
    if shape == 'circle':
        return circle(**params)
    if shape == 'ellipse':
        return ellipse(**params)
    if shape == 'contour':
        return contour(**params)
    if shape == 'sphere':
        return sphere(**params)
    if shape == 'cube':
        return cube(**params)

def circle(**params):
    now = datetime.now().strftime('%H%M%S')
    # sample case
    if not params:
        params = {'center': (0,0), 'radius': 0.5, 'color': 'g', 'sample': True}
    else:
        params.update(ps.CIRCLEPARAM)
    # circle
    circle = plt.Circle(params['center'], params['radius'], color=params['color'], clip_on=False)
    # figure
    fig = plt.gcf()
    ax = fig.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.xlim(params['center'][0] - params['radius'] * 2, params['center'][0] + params['radius'] * 2)
    plt.ylim(params['center'][1] - params['radius'] * 2, params['center'][1] + params['radius'] * 2)
    # plot artist
    ax.add_artist(circle)
    # save file
    if params['sample']:
        fig.savefig('sample_circle.png')
        # reset plot
        plt.close()
        return
    else:
        filename_part = 'circle' + now + '.png'
        filename = os.path.join(os.getcwd(), params['dirr'], filename_part)
        fig.savefig(filename)
        # reset plot
        plt.close()
        return filename_part, params

def ellipse(**params):
    now = datetime.now().strftime('%H%M%S')
    params.update(ps.ELLIPSEPARAM)
    # ellipse
    ellipse = Ellipse(xy=params['center'], width=params['width'], height=params['height'], color=params['color'], clip_on=False)
    # figure
    fig = plt.gcf()
    ax = fig.gca()
    ax.set_aspect('equal', adjustable='box')
    dominant = params['width'] if params['width'] > params['height'] else params['height']
    plt.xlim(params['center'][0] - dominant * 2, params['center'][0] + dominant * 2)
    plt.ylim(params['center'][1] - dominant * 2, params['center'][1] + dominant * 2)
    # plot artist
    ax.add_artist(ellipse)
    # save file
    filename_part = 'ellipse' + now + '.png'
    filename = os.path.join(os.getcwd(), params['dirr'], filename_part)
    fig.savefig(filename)
    # reset plot
    plt.close()
    return filename_part, params

def contour(**params):
    now = datetime.now().strftime('%H%M%S')
    params.update(ps.CONTOURPARAM)
    # contour
    pathpoints = params['bezierpoints'] * params['edges'] + 1
    angles = np.linspace(0, 2*np.pi, pathpoints)
    codes = np.full(pathpoints, Path.CURVE4)
    codes[0] = Path.MOVETO
    verts = np.stack((np.cos(angles), np.sin(angles))).T * (2 * params['perturbation'] * np.random.random(pathpoints) + 1 - params['perturbation'])[:,None]
    verts[-1,:] = verts[0,:]
    path = Path(verts, codes)
    # figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    patch = patches.PathPatch(path, facecolor=params['color'], lw=2)
    ax.add_patch(patch)
    ax.set_xlim(np.min(verts)*2, np.max(verts)*2)
    ax.set_ylim(np.min(verts)*2, np.max(verts)*2)
    # to emphasize contour's shape axis is turned off
    ax.axis('off')
    # save file
    filename_part = 'contour' + now + '.png'
    filename = os.path.join(os.getcwd(), params['dirr'], filename_part)
    fig.savefig(filename)
    # reset plot
    plt.close()
    return filename_part, params

def sphere(**params):
    now = datetime.now().strftime('%H%M%S')
    params.update(ps.SPHEREPARAM)
    # 3D plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal", adjustable='box')
    # sphere
    radius = params['radius']
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
    x = radius * np.cos(u) * np.sin(v) + params['center'][0]
    y = radius * np.sin(u) * np.sin(v) + params['center'][1]
    z = radius * np.cos(v) + params['center'][2]
    ax.plot_wireframe(x, y, z, color='r')
    ax.plot_surface(x, y, z, color=params['color'], alpha=0.5)
    # save file
    filename_part = 'sphere' + now + '.png'
    filename = os.path.join(os.getcwd(), params['dirr'], filename_part)
    fig.savefig(filename)
    # reset plot
    plt.close()
    return filename_part, params

def cube(**params):
    now = datetime.now().strftime('%H%M%S')
    params.update(ps.CUBEPARAM)
    # 3D plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect("equal", adjustable='box')
    # cube
    ### for the sake of simplicity in code and considering the fact that drawing a cube
    ### would not much be needed for the research, center coordinate has single value for
    ### all x,y,z
    r = [params['center'] - params['radius'], params['center'] + params['radius']]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        # among all possible combinations select only the needed
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot3D(*zip(s, e), color=params['color'])
    # save file
    filename_part = 'cube' + now + '.png'
    filename = os.path.join(os.getcwd(), params['dirr'], filename_part)
    fig.savefig(filename)
    # reset plot
    plt.close()
    return filename_part, params