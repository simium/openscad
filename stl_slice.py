import stl
from stl import mesh
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

def poi(slice_normal, slice_point, ray_p, ray_d):
    epsilon=1e-6

    ndotu = slice_normal.dot(ray_d)

    if abs(ndotu) < epsilon:
        #print ("No intersection or line is within plane")
        return None

    w = ray_p - slice_point
    si = -slice_normal.dot(w) / ndotu
    Psi = w + si * ray_d + slice_point
    return Psi

def direction_vector(A, B, verbose=False):
    dist = B - A
    norm = math.sqrt(dist[0] ** 2 + dist[1] ** 2 + dist[2] ** 2)

    dir_v = dist/norm

    if verbose:
        print "dir_v: [%.3f,%.3f,%.3f]" % (dir_v[0], dir_v[1], dir_v[2])

    return dir_v

# Load the STL file
my_stl_mesh = mesh.Mesh.from_file('stormtrooper_lowpoly_body.stl')
#my_stl_mesh = mesh.Mesh.from_file('sphere_10mm.stl')

print "Num of points:", 3*len(my_stl_mesh.vectors)

# Find its bounding box
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(my_stl_mesh)
print minx, maxx, miny, maxy, minz, maxz

for v in my_stl_mesh.vectors:
    for p in v:
        p[0] = p[0] + abs(minx)
        p[1] = p[1] + abs(miny)
        p[2] = p[2] + abs(minz)

minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(my_stl_mesh)
print minx, maxx, miny, maxy, minz, maxz

slice_step = 3
steps = np.arange(minz+slice_step, maxz+slice_step, slice_step)

x = []
y = []
z = []

for step in steps:
    slice_normal = np.array([0,0,1])
    slice_point = np.array([0,0,step])

    pois = 0

    for v in my_stl_mesh.vectors:
        Adir = np.array(direction_vector(v[0], v[1]))
        Bdir = np.array(direction_vector(v[1], v[2]))
        Cdir = np.array(direction_vector(v[2], v[0]))

        p = poi(slice_normal, slice_point, v[0], Adir)

        if p is not None:
            pois = pois + 1
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])

        p = poi(slice_normal, slice_point, v[1], Bdir)

        if p is not None:
            pois = pois + 1
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])

        p = poi(slice_normal, slice_point, v[2], Cdir)

        if p is not None:
            pois = pois + 1
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])

    #print "Found %d points of intersection at z = %.3f" % (pois, step)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, c='r')
#x, y = np.meshgrid(x, y)
#ax.plot_surface(x, y, z, color='b')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
