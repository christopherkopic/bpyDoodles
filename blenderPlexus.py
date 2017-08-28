#Blender Plexus
#The (in)famous Plexus effect recreated in Blender3d
#Written by Christopher Kopic in August 2017

#Manual:
#Select any Mesh Object
#Tab into Edit Mode
#Select everything and delete only Edges and Faces
#(You should be left with the vertices of the mesh only)
#Tab into Object Mode
#Run the script
#Hit Ctrl-Z, tweak the radius variable and run script again to get desired result

#Warning:
#Big radius values may lead to very long compute times
#Safe your file before running the script, so you can force quit blender and try again

import bpy
import bmesh
import mathutils

ori = bmesh.new()
me = bpy.context.object.data
ori.from_mesh(me)

# create kd-Tree
ori.verts.ensure_lookup_table()
size = len(ori.verts)
kd = mathutils.kdtree.KDTree(size)

for i, v in enumerate(ori.verts):
    kd.insert(v.co, i)

kd.balance()

# create connections
radius = 0.2
for vert in ori.verts:
    for (co, index, dist) in kd.find_range(vert.co, radius):
        if vert.index != index:
            bmesh.ops.contextual_create(ori, geom=[vert, ori.verts[index]])

# apply changes
ori.to_mesh(me)
ori.free()
