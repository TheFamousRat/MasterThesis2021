# https://towardsdatascience.com/blender-2-8-grease-pencil-scripting-and-generative-art-cbbfd3967590

import bpy
import math
import numpy as np

def get_grease_pencil(gpencil_obj_name='GPencil') -> bpy.types.GreasePencil:
    """
    Return the grease-pencil object with the given name. Initialize one if not already present.
    :param gpencil_obj_name: name/key of the grease pencil object in the scene
    """

    # If not present already, create grease pencil object
    if gpencil_obj_name not in bpy.context.scene.objects:
        bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
        # rename grease pencil
        bpy.context.scene.objects[-1].name = gpencil_obj_name

    # Get grease pencil object
    gpencil = bpy.context.scene.objects[gpencil_obj_name]

    return gpencil


def get_grease_pencil_layer(gpencil: bpy.types.GreasePencil, gpencil_layer_name='GP_Layer',
                            clear_layer=False) -> bpy.types.GPencilLayer:
    """
    Return the grease-pencil layer with the given name. Create one if not already present.
    :param gpencil: grease-pencil object for the layer data
    :param gpencil_layer_name: name/key of the grease pencil layer
    :param clear_layer: whether to clear all previous layer data
    """

    # Get grease pencil layer or create one if none exists
    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)

    if clear_layer:
        gpencil_layer.clear()  # clear all previous layer data

    # bpy.ops.gpencil.paintmode_toggle()  # need to trigger otherwise there is no frame

    return gpencil_layer


# Util for default behavior merging previous two methods
def init_grease_pencil(gpencil_obj_name='GPencil', gpencil_layer_name='GP_Layer',
                       clear_layer=True) -> bpy.types.GPencilLayer:
    gpencil = get_grease_pencil(gpencil_obj_name)
    gpencil_layer = get_grease_pencil_layer(gpencil, gpencil_layer_name, clear_layer=clear_layer)
    return gpencil, gpencil_layer

def getGPColorMaterialIdx(gpencil, colorHex):
    """
    Returns a found or created stroke material with the RGB color corresponding to the given HEX code
    """
    shaderName = "GP_{}".format(colorHex)
    if not shaderName in bpy.data.materials:
        newMat = bpy.data.materials.new(shaderName)
        bpy.data.materials.create_gpencil_data(newMat)
        rgb = tuple(int(colorHex[i:i+2], 16) for i in (0, 2, 4))
        
        for i in range(3):
            newMat.grease_pencil.color[i] = rgb[i]
        newMat.grease_pencil.color[3] = 1

    gpMat = bpy.data.materials[shaderName]

    if not gpMat.name in gpencil.data.materials:
        gpencil.data.materials.append(gpMat)

    return gpencil.material_slots.find(gpMat.name)

def draw_line(gpencil, gp_frame, pointsArr, pointsSize, colorHex):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'  # allows for editing

    # Define stroke geometry
    gp_stroke.points.add(count=len(pointsArr))
    for i in range(len(pointsArr)):
        point = gp_stroke.points[i]
        point.co = pointsArr[i]
        point.pressure = pointsSize[i]

    #Getting (creating) a material corresponding to the required color
    gp_stroke.material_index = getGPColorMaterialIdx(gpencil, colorHex)

    return gp_stroke