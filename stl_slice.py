import stl
from stl import mesh
import numpy as np
import math
import svgwrite
from svgwrite import mm, cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def find_mins_maxs(obj):
    """ Computes bounding box of the mesh """
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
    """ Computes point of intersection of plane and line, None if it does not intersect """
    epsilon=1e-6

    ndotu = slice_normal.dot(ray_d)

    if abs(ndotu) < epsilon:
        return None

    w = ray_p - slice_point
    si = -slice_normal.dot(w) / ndotu
    Psi = w + si * ray_d + slice_point

    return Psi

def point_between_points(p, v1, v2):
    """ Returns True if p[z] is located between v1[z] and v2[z] """
    if v1[2] > v2[2]:
        return v1[2] > p[2] and p[2] > v2[2]
    elif v1[2] < v2[2]:
        return v1[2] < p[2] and p[2] < v2[2]
    else:
        return False

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def is_left(p, v1, v2):
    """ Returns True if point p is left of line v1-v2 """
    a = np.array([[v1[0]-p[0], v2[0]-p[0]], [v1[1]-p[1], v2[1]-p[1]]])
    return np.linalg.det(a) < 0

# Load the STL file
#my_stl_mesh = mesh.Mesh.from_file('Nefertiti-hollow.stl')
#my_stl_mesh = mesh.Mesh.from_file('sphere_10mm.stl')
my_stl_mesh = mesh.Mesh.from_file('prism_10mm.stl')
#my_stl_mesh = mesh.Mesh.from_file('cube_10mm.stl')

print "+Model info:"
print "|-Num. of vertex:", 3*len(my_stl_mesh.vectors)

# Find its bounding box
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(my_stl_mesh)

for v in my_stl_mesh.vectors:
    for p in v:
        p[0] = p[0] - minx
        p[1] = p[1] - miny
        p[2] = p[2] - minz

# Find its bounding box
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(my_stl_mesh)
print "|-X min=%.3f, X max=%.3f, Y min=%.3f, Y max=%.3f, Z min=%.3f, Z max=%.3f" % (minx, maxx, miny, maxy, minz, maxz)
print "|-Dimensions (WxDxH): %.3fx%.3fx%.3f" % (maxx-minx, maxy-miny, maxz-minz)

# Testing heights for slicing
slice_step = (maxz-minz)/10
if slice_step < 1.0:
    slice_step = 1.0
steps = np.arange(minz+slice_step, maxz+slice_step, slice_step)

# Needed for plotting
plotX = []
plotY = []
plotZ = []

step_iteration = 0

# At each height, compute the lines that intersect the plane at that given height
for step in steps:
    slice_normal = np.array([0,0,1])
    slice_point = np.array([0,0,step])

    print "Processing intersection plane at height %.3f mm..." % (step)

    pois = 0
    layer = []

    for v in my_stl_mesh.vectors:
        Adir = unit_vector(v[1]-v[0])
        p = poi(slice_normal, slice_point, v[0], Adir)
        if p is not None and point_between_points(p, v[0], v[1]):
            pois = pois + 1
            plotX.append(p[0])
            plotY.append(p[1])
            plotZ.append(p[2])
            layer.append((p[0],p[1]))

        Bdir = unit_vector(v[2]-v[1])
        p = poi(slice_normal, slice_point, v[1], Bdir)
        if p is not None and point_between_points(p, v[1], v[2]):
            pois = pois + 1
            plotX.append(p[0])
            plotY.append(p[1])
            plotZ.append(p[2])
            layer.append((p[0],p[1]))

        Cdir = unit_vector(v[0]-v[2])
        p = poi(slice_normal, slice_point, v[2], Cdir)
        if p is not None and point_between_points(p, v[2], v[0]):
            pois = pois + 1
            plotX.append(p[0])
            plotY.append(p[1])
            plotZ.append(p[2])
            layer.append((p[0],p[1]))

    if pois > 0:

        # Implements gift wrapping algorithm to create convex hull
        point_on_hull = layer[0]

        ordered_layer = []

        for l in layer:
            if l[0] < point_on_hull[0]:
                point_on_hull = l

        while True:
            ordered_layer.append(point_on_hull)
            endpoint = layer[0]
            for l in layer:
                if endpoint == point_on_hull or is_left(l, point_on_hull, endpoint):
                    endpoint = l
            point_on_hull = endpoint
            if endpoint == ordered_layer[0]:
                break

        sizeX = '%dmm' % (int(maxx)+1)
        sizeY = '%dmm' % (int(maxy)+1)
        dwg = svgwrite.Drawing('test_%d.svg' % step_iteration, size=(sizeX, sizeY), viewBox=('0 0 %d %d' % (int(maxx)+1, int(maxy)+1)))

        my_polygon = dwg.add(dwg.polygon(ordered_layer, stroke='black'))
        my_polygon.fill('none')
        dwg.save()

    step_iteration = step_iteration + 1

print "+ Slice results:"
print "|-Intersection points found: %d" % (len(plotZ))

# Plot
do_plot = True

if do_plot:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(plotX, plotY, plotZ, c='r')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
