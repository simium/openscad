import stl
from stl import mesh
import numpy as np
import math
from dxfwrite import DXFEngine as dxf
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from PIL import Image

# Computes bounding box of the mesh
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

# Computes point of intersection of plane and line, None if it does not intersect
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

# Computes direction vector
def direction_vector(A, B, verbose=False):
    dist = B - A
    norm = math.sqrt(dist[0] ** 2 + dist[1] ** 2 + dist[2] ** 2)

    dir_v = dist/norm

    if verbose:
        print "dir_v: [%.3f,%.3f,%.3f]" % (dir_v[0], dir_v[1], dir_v[2])

    return dir_v

def point_between_points(p, v1, v2):
    if v1[2] > v2[2]:
        return v1[2] > p[2] and p[2] > v2[2]
    elif v1[2] < v2[2]:
        return v1[2] < p[2] and p[2] < v2[2]
    else:
        return False

# Load the STL file
my_stl_mesh = mesh.Mesh.from_file('stormtrooper_lowpoly_head.stl')
#my_stl_mesh = mesh.Mesh.from_file('sphere_10mm.stl')
#my_stl_mesh = mesh.Mesh.from_file('prism_10mm.stl')
#my_stl_mesh = mesh.Mesh.from_file('cube_10mm.stl')

print "+Model info:"
print "|-Num. of vertex:", 3*len(my_stl_mesh.vectors)

# Find its bounding box
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(my_stl_mesh)
print "|-X min=%.3f, X max=%.3f, Y min=%.3f, Y max=%.3f, Z min=%.3f, Z max=%.3f" % (minx, maxx, miny, maxy, minz, maxz)
print "|-Dimensions (WxDxH): %.3fx%.3fx%.3f" % (maxx-minx, maxy-miny, maxz-minz)

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
#slice_step = (maxz-minz)/10
slice_step = 2
steps = np.arange(minz, maxz+slice_step, slice_step)

# Needed for plotting
plotX = []
plotY = []
plotZ = []

step_iteration = 0

img = Image.new( 'RGB', (10*int(maxx)+1,10*int(maxy)+1), "white") # create a new black image
pixels = img.load() # create the pixel map

# At each height, compute the lines that intersect the plane at that given height
for step in steps:
    slice_normal = np.array([0,0,1])
    slice_point = np.array([0,0,step])

    pois = 0

    layer = []

    for v in my_stl_mesh.vectors:
        Adir = np.array(direction_vector(v[0], v[1]))
        p = poi(slice_normal, slice_point, v[0], Adir)
        if p is not None and point_between_points(p, v[0], v[1]):
            pois = pois + 1
            plotX.append(p[0])
            plotY.append(p[1])
            plotZ.append(p[2])
            layer.append([p[0], p[1]])

        Bdir = np.array(direction_vector(v[1], v[2]))
        p = poi(slice_normal, slice_point, v[1], Bdir)
        if p is not None and point_between_points(p, v[1], v[2]):
            pois = pois + 1
            plotX.append(p[0])
            plotY.append(p[1])
            plotZ.append(p[2])
            layer.append([p[0], p[1]])

        Cdir = np.array(direction_vector(v[2], v[0]))
        p = poi(slice_normal, slice_point, v[2], Cdir)
        if p is not None and point_between_points(p, v[2], v[0]):
            pois = pois + 1
            plotX.append(p[0])
            plotY.append(p[1])
            plotZ.append(p[2])
            layer.append([p[0], p[1]])

    if pois > 0:
        for p in layer:
            try:
                pixels[10*int(p[0]),10*int(p[1])] = (200, 200, 200)
            except:
                print p[0], p[1]

        #drawing = dxf.drawing('layer_%d.dxf' % step_iteration)
        #layer_tup = zip(layer, layer[1:] + [layer[0]])

        #for p1, p2 in zip(layer, layer[1:] + [layer[0]]):
        #    drawing.add(dxf.line((p1[0], p1[1]), (p2[0], p2[1]), color=0))

        #drawing.add_layer('LAYER_%d' % step_iteration, color=7)
        #drawing.save()

    step_iteration = step_iteration + 1

img.show()

print "+ Slice results:"
print "|-Intersection points found: %d" % (len(plotZ))

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(plotX, plotY, plotZ, c='r')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
