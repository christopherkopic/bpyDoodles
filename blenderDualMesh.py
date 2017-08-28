#Blender Dual Mesh
#Creates a dual graph like mesh based on another mesh object.
#Written by Christopher Kopic in august 2017.

#Manual:
#Select a Mesh Object in Object Mode.
#Run the Script.
#Works best on triangle meshes without holes.

#Warning:
#Computation time may be very long on dense meshes.

import bpy
import bmesh

ori = bmesh.new()
dual = bmesh.new()
ori.from_mesh(bpy.context.object.data)

#create verts
ori.faces.ensure_lookup_table()
for face in ori.faces:
    bmesh.ops.create_vert(dual, co = face.calc_center_median())
dual.verts.ensure_lookup_table()

#create edges
ori.edges.ensure_lookup_table()
for edge in ori.edges:
    if edge.is_boundary == False:
        new_edge = []
        for face in edge.link_faces:
            new_edge.append(dual.verts[face.index])
        bmesh.ops.contextual_create(dual, geom = new_edge)
dual.edges.ensure_lookup_table()

#create faces
bmesh.ops.edgenet_fill(dual, edges = dual.edges)

# Finish up, write the bmesh into a new mesh
ori.free()
me = bpy.data.meshes.new("DualMesh")
dual.to_mesh(me)
dual.free()

# Add the mesh to the scene
scene = bpy.context.scene
obj = bpy.data.objects.new("DualObject", me)
scene.objects.link(obj)

# Select and make active
scene.objects.active = obj
obj.select = True
