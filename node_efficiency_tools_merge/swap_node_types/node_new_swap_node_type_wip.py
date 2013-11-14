bl_info = {
    'name': "Swap Node Type",
    'author': "Bartek Skorupa",
    'version': (0, 1),
    'blender': (2, 6, 9),
    'location': "Ctrt Alt Shift S",
    'description': "for tests",
    'warning': "",
    'wiki_url': "",
    'tracker_url': "",
    'category': "Node",
    }

import bpy
import blf
import bgl
from bpy.types import Operator, Panel, Menu
from bpy.props import FloatProperty, EnumProperty, BoolProperty, StringProperty, FloatVectorProperty
from mathutils import Vector
from math import cos, sin, pi, sqrt

# shader nodes
# (rna_type.identifier, type, rna_type.name)
shaders_input_nodes_props = (
    ('ShaderNodeTexCoord', 'TEX_COORD', 'Texture Coordinate'),
    ('ShaderNodeAttribute', 'ATTRIBUTE', 'Attribute'),
    ('ShaderNodeLightPath', 'LIGHT_PATH', 'Light Path'),
    ('ShaderNodeFresnel', 'FRESNEL', 'Fresnel'),
    ('ShaderNodeLayerWeight', 'LAYER_WEIGHT', 'Layer Weight'),
    ('ShaderNodeRGB', 'RGB', 'RGB'),
    ('ShaderNodeValue', 'VALUE', 'Value'),
    ('ShaderNodeTangent', 'TANGENT', 'Tangent'),
    ('ShaderNodeNewGeometry', 'NEW_GEOMETRY', 'Geometry'),
    ('ShaderNodeWireframe', 'WIREFRAME', 'Wireframe'),
    ('ShaderNodeObjectInfo', 'OBJECT_INFO', 'Object Info'),
    ('ShaderNodeHairInfo', 'HAIR_INFO', 'Hair Info'),
    ('ShaderNodeParticleInfo', 'PARTICLE_INFO', 'Particle Info'),
    ('ShaderNodeCameraData', 'CAMERA', 'Camera Data'),
    )
# (rna_type.identifier, type, rna_type.name)
shaders_output_nodes_props = (
    ('ShaderNodeOutputMaterial', 'OUTPUT_MATERIAL', 'Material Output'),
    ('ShaderNodeOutputLamp', 'OUTPUT_LAMP', 'Lamp Output'),
    ('ShaderNodeOutputWorld', 'OUTPUT_WORLD', 'World Output'),
    )
# (rna_type.identifier, type, rna_type.name)
shaders_shader_nodes_props = (
    ('ShaderNodeMixShader', 'MIX_SHADER', 'Mix Shader'),
    ('ShaderNodeAddShader', 'ADD_SHADER', 'Add Shader'),
    ('ShaderNodeBsdfDiffuse', 'BSDF_DIFFUSE', 'Diffuse BSDF'),
    ('ShaderNodeBsdfGlossy', 'BSDF_GLOSSY', 'Glossy BSDF'),
    ('ShaderNodeBsdfTransparent', 'BSDF_TRANSPARENT', 'Transparent BSDF'),
    ('ShaderNodeBsdfRefraction', 'BSDF_REFRACTION', 'Refraction BSDF'),
    ('ShaderNodeBsdfGlass', 'BSDF_GLASS', 'Glass BSDF'),
    ('ShaderNodeBsdfTranslucent', 'BSDF_TRANSLUCENT', 'Translucent BSDF'),
    ('ShaderNodeBsdfAnisotropic', 'BSDF_ANISOTROPIC', 'Anisotropic BSDF'),
    ('ShaderNodeBsdfVelvet', 'BSDF_VELVET', 'Velvet BSDF'),
    ('ShaderNodeBsdfToon', 'BSDF_TOON', 'Toon BSDF'),
    ('ShaderNodeSubsurfaceScattering', 'SUBSURFACE_SCATTERING', 'Subsurface Scattering'),
    ('ShaderNodeEmission', 'EMISSION', 'Emission'),
    ('ShaderNodeBackground', 'BACKGROUND', 'Background'),
    ('ShaderNodeAmbientOcclusion', 'AMBIENT_OCCLUSION', 'Ambient Occlusion'),
    ('ShaderNodeHoldout', 'HOLDOUT', 'Holdout'),
    )
# (rna_type.identifier, type, rna_type.name)
shaders_texture_nodes_props = (
    ('ShaderNodeTexImage', 'TEX_IMAGE', 'Image'),
    ('ShaderNodeTexEnvironment', 'TEX_ENVIRONMENT', 'Environment'),
    ('ShaderNodeTexSky', 'TEX_SKY', 'Sky'),
    ('ShaderNodeTexNoise', 'TEX_NOISE', 'Noise'),
    ('ShaderNodeTexWave', 'TEX_WAVE', 'Wave'),
    ('ShaderNodeTexVoronoi', 'TEX_VORONOI', 'Voronoi'),
    ('ShaderNodeTexMusgrave', 'TEX_MUSGRAVE', 'Musgrave'),
    ('ShaderNodeTexGradient', 'TEX_GRADIENT', 'Gradient'),
    ('ShaderNodeTexMagic', 'TEX_MAGIC', 'Magic'),
    ('ShaderNodeTexChecker', 'TEX_CHECKER', 'Checker'),
    ('ShaderNodeTexBrick', 'TEX_BRICK', 'Brick')
    )
# (rna_type.identifier, type, rna_type.name)
shaders_color_nodes_props = (
    ('ShaderNodeMixRGB', 'MIX_RGB', 'MixRGB'),
    ('ShaderNodeRGBCurve', 'CURVE_RGB', 'RGB Curves'),
    ('ShaderNodeInvert', 'INVERT', 'Invert'),
    ('ShaderNodeLightFalloff', 'LIGHT_FALLOFF', 'Light Falloff'),
    ('ShaderNodeHueSaturation', 'HUE_SAT', 'Hue/Saturation'),
    ('ShaderNodeGamma', 'GAMMA', 'Gamma'),
    ('ShaderNodeBrightContrast', 'BRIGHTCONTRAST', 'Bright Contrast'),
    )
# (rna_type.identifier, type, rna_type.name)
shaders_vector_nodes_props = (
    ('ShaderNodeMapping', 'MAPPING', 'Mapping'),
    ('ShaderNodeBump', 'BUMP', 'Bump'),
    ('ShaderNodeNormalMap', 'NORMAL_MAP', 'Normal Map'),
    ('ShaderNodeNormal', 'NORMAL', 'Normal'),
    ('ShaderNodeVectorCurve', 'CURVE_VEC', 'Vector Curves'),
    ('ShaderNodeVectorTransform', 'VECT_TRANSFORM', 'Vector Transform'),
    )
# (rna_type.identifier, type, rna_type.name)
shaders_converter_nodes_props = (
    ('ShaderNodeMath', 'MATH', 'Math'),
    ('ShaderNodeValToRGB', 'VALTORGB', 'ColorRamp'),
    ('ShaderNodeRGBToBW', 'RGBTOBW', 'RGB to BW'),
    ('ShaderNodeVectorMath', 'VECT_MATH', 'Vector Math'),
    ('ShaderNodeSeparateRGB', 'SEPRGB', 'Separate RGB'),
    ('ShaderNodeCombineRGB', 'COMBRGB', 'Combine RGB'),
    ('ShaderNodeSeparateHSV', 'SEPHSV', 'Separate HSV'),
    ('ShaderNodeCombineHSV', 'COMBHSV', 'Combine HSV'),
    ('ShaderNodeWavelength', 'WAVELENGTH', 'Wavelength'),
    ('ShaderNodeBlackbody', 'BLACKBODY', 'Blackbody'),
    )
# (rna_type.identifier, type, rna_type.name)
shaders_layout_nodes_props = (
    ('NodeFrame', 'FRAME', 'Frame'),
    ('NodeReroute', 'REROUTE', 'Reroute'),
    )

# compositing nodes
# (rna_type.identifier, type, rna_type.name)
compo_input_nodes_props = (
    ('CompositorNodeRLayers', 'R_LAYERS', 'Render Layers'),
    ('CompositorNodeImage', 'IMAGE', 'Image'),
    ('CompositorNodeMovieClip', 'MOVIECLIP', 'Movie Clip'),
    ('CompositorNodeMask', 'MASK', 'Mask'),
    ('CompositorNodeRGB', 'RGB', 'RGB'),
    ('CompositorNodeValue', 'VALUE', 'Value'),
    ('CompositorNodeTexture', 'TEXTURE', 'Texture'),
    ('CompositorNodeBokehImage', 'BOKEHIMAGE', 'Bokeh Image'),
    ('CompositorNodeTime', 'TIME', 'Time'),
    ('CompositorNodeTrackPos', 'TRACKPOS', 'Track Position'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_output_nodes_props = (
    ('CompositorNodeComposite', 'COMPOSITE', 'Composite'),
    ('CompositorNodeViewer', 'VIEWER', 'Viewer'),
    ('CompositorNodeSplitViewer', 'SPLITVIEWER', 'Split Viewer'),
    ('CompositorNodeOutputFile', 'OUTPUT_FILE', 'File Output'),
    ('CompositorNodeLevels', 'LEVELS', 'Levels'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_color_nodes_props = (
    ('CompositorNodeMixRGB', 'MIX_RGB', 'Mix'),
    ('CompositorNodeAlphaOver', 'ALPHAOVER', 'Alpha Over'),
    ('CompositorNodeInvert', 'INVERT', 'Invert'),
    ('CompositorNodeCurveRGB', 'CURVE_RGB', 'RGB Curves'),
    ('CompositorNodeHueSat', 'HUE_SAT', 'Hue Saturation Value'),
    ('CompositorNodeColorBalance', 'COLORBALANCE', 'Color Balance'),
    ('CompositorNodeHueCorrect', 'HUECORRECT', 'Hue Correct'),
    ('CompositorNodeBrightContrast', 'BRIGHTCONTRAST', 'Bright/Contrast'),
    ('CompositorNodeGamma', 'GAMMA', 'Gamma'),
    ('CompositorNodeColorCorrection', 'COLORCORRECTION', 'Color Correction'),
    ('CompositorNodeTonemap', 'TONEMAP', 'Tonemap'),
    ('CompositorNodeZcombine', 'ZCOMBINE', 'Z Combine'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_converter_nodes_props = (
    ('CompositorNodeMath', 'MATH', 'Math'),
    ('CompositorNodeValToRGB', 'VALTORGB', 'ColorRamp'),
    ('CompositorNodeSetAlpha', 'SETALPHA', 'Set Alpha'),
    ('CompositorNodePremulKey', 'PREMULKEY', 'Alpha Convert'),
    ('CompositorNodeIDMask', 'ID_MASK', 'ID Mask'),
    ('CompositorNodeRGBToBW', 'RGBTOBW', 'RGB to BW'),
    ('CompositorNodeSepRGBA', 'SEPRGBA', 'Separate RGBA'),
    ('CompositorNodeCombRGBA', 'COMBRGBA', 'Combine RGBA'),
    ('CompositorNodeSepHSVA', 'SEPHSVA', 'Separate HSVA'),
    ('CompositorNodeCombHSVA', 'COMBHSVA', 'Combine HSVA'),
    ('CompositorNodeSepYUVA', 'SEPYUVA', 'Separate YUVA'),
    ('CompositorNodeCombYUVA', 'COMBYUVA', 'Combine YUVA'),
    ('CompositorNodeSepYCCA', 'SEPYCCA', 'Separate YCbCrA'),
    ('CompositorNodeCombYCCA', 'COMBYCCA', 'Combine YCbCrA'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_filter_nodes_props = (
    ('CompositorNodeBlur', 'BLUR', 'Blur'),
    ('CompositorNodeBilateralblur', 'BILATERALBLUR', 'Bilateral Blur'),
    ('CompositorNodeDilateErode', 'DILATEERODE', 'Dilate/Erode'),
    ('CompositorNodeDespeckle', 'DESPECKLE', 'Despeckle'),
    ('CompositorNodeFilter', 'FILTER', 'Filter'),
    ('CompositorNodeBokehBlur', 'BOKEHBLUR', 'Bokeh Blur'),
    ('CompositorNodeVecBlur', 'VECBLUR', 'Vector Blur'),
    ('CompositorNodeDefocus', 'DEFOCUS', 'Defocus'),
    ('CompositorNodeGlare', 'GLARE', 'Glare'),
    ('CompositorNodeInpaint', 'INPAINT', 'Inpaint'),
    ('CompositorNodeDBlur', 'DBLUR', 'Directional Blur'),
    ('CompositorNodePixelate', 'PIXELATE', 'Pixelate'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_vector_nodes_props = (
    ('CompositorNodeNormal', 'NORMAL', 'Normal'),
    ('CompositorNodeMapValue', 'MAP_VALUE', 'Map Value'),
    ('CompositorNodeMapRange', 'MAP_RANGE', 'Map Range'),
    ('CompositorNodeNormalize', 'NORMALIZE', 'Normalize'),
    ('CompositorNodeCurveVec', 'CURVE_VEC', 'Vector Curves'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_matte_nodes_props = (
    ('CompositorNodeKeying', 'KEYING', 'Keying'),
    ('CompositorNodeKeyingScreen', 'KEYINGSCREEN', 'Keying Screen'),
    ('CompositorNodeChannelMatte', 'CHANNEL_MATTE', 'Channel Key'),
    ('CompositorNodeColorSpill', 'COLOR_SPILL', 'Color Spill'),
    ('CompositorNodeBoxMask', 'BOXMASK', 'Box Mask'),
    ('CompositorNodeEllipseMask', 'ELLIPSEMASK', 'Ellipse Mask'),
    ('CompositorNodeLumaMatte', 'LUMA_MATTE', 'Luminance Key'),
    ('CompositorNodeDiffMatte', 'DIFF_MATTE', 'Difference Key'),
    ('CompositorNodeDistanceMatte', 'DISTANCE_MATTE', 'Distance Key'),
    ('CompositorNodeChromaMatte', 'CHROMA_MATTE', 'Chroma Key'),
    ('CompositorNodeColorMatte', 'COLOR_MATTE', 'Color Key'),
    ('CompositorNodeDoubleEdgeMask', 'DOUBLEEDGEMASK', 'Double Edge Mask'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_distort_nodes_props = (
    ('CompositorNodeScale', 'SCALE', 'Scale'),
    ('CompositorNodeLensdist', 'LENSDIST', 'Lens Distortion'),
    ('CompositorNodeMovieDistortion', 'MOVIEDISTORTION', 'Movie Distortion'),
    ('CompositorNodeTranslate', 'TRANSLATE', 'Translate'),
    ('CompositorNodeRotate', 'ROTATE', 'Rotate'),
    ('CompositorNodeFlip', 'FLIP', 'Flip'),
    ('CompositorNodeCrop', 'CROP', 'Crop'),
    ('CompositorNodeDisplace', 'DISPLACE', 'Displace'),
    ('CompositorNodeMapUV', 'MAP_UV', 'Map UV'),
    ('CompositorNodeTransform', 'TRANSFORM', 'Transform'),
    ('CompositorNodeStabilize', 'STABILIZE2D', 'Stabilize 2D'),
    ('CompositorNodePlaneTrackDeform', 'PLANETRACKDEFORM', 'Plane Track Deform'),
    )
# (rna_type.identifier, type, rna_type.name)
compo_layout_nodes_props = (
    ('NodeFrame', 'FRAME', 'Frame'),
    ('NodeReroute', 'REROUTE', 'Reroute'),
    ('CompositorNodeSwitch', 'SWITCH', 'Switch'),
    )
# list of blend types of "Mix" nodes in a form that can be used as 'items' for EnumProperty.
# used list, not tuple for easy merging with other lists.
blend_types = [
    ('MIX', 'Mix', 'Mix Mode'),
    ('ADD', 'Add', 'Add Mode'),
    ('MULTIPLY', 'Multiply', 'Multiply Mode'),
    ('SUBTRACT', 'Subtract', 'Subtract Mode'),
    ('SCREEN', 'Screen', 'Screen Mode'),
    ('DIVIDE', 'Divide', 'Divide Mode'),
    ('DIFFERENCE', 'Difference', 'Difference Mode'),
    ('DARKEN', 'Darken', 'Darken Mode'),
    ('LIGHTEN', 'Lighten', 'Lighten Mode'),
    ('OVERLAY', 'Overlay', 'Overlay Mode'),
    ('DODGE', 'Dodge', 'Dodge Mode'),
    ('BURN', 'Burn', 'Burn Mode'),
    ('HUE', 'Hue', 'Hue Mode'),
    ('SATURATION', 'Saturation', 'Saturation Mode'),
    ('VALUE', 'Value', 'Value Mode'),
    ('COLOR', 'Color', 'Color Mode'),
    ('SOFT_LIGHT', 'Soft Light', 'Soft Light Mode'),
    ('LINEAR_LIGHT', 'Linear Light', 'Linear Light Mode'),
    ]
# list of operations of "Math" nodes in a form that can be used as 'items' for EnumProperty.
# used list, not tuple for easy merging with other lists.
operations = [
    ('ADD', 'Add', 'Add Mode'),
    ('MULTIPLY', 'Multiply', 'Multiply Mode'),
    ('SUBTRACT', 'Subtract', 'Subtract Mode'),
    ('DIVIDE', 'Divide', 'Divide Mode'),
    ('SINE', 'Sine', 'Sine Mode'),
    ('COSINE', 'Cosine', 'Cosine Mode'),
    ('TANGENT', 'Tangent', 'Tangent Mode'),
    ('ARCSINE', 'Arcsine', 'Arcsine Mode'),
    ('ARCCOSINE', 'Arccosine', 'Arccosine Mode'),
    ('ARCTANGENT', 'Arctangent', 'Arctangent Mode'),
    ('POWER', 'Power', 'Power Mode'),
    ('LOGARITHM', 'Logatithm', 'Logarithm Mode'),
    ('MINIMUM', 'Minimum', 'Minimum Mode'),
    ('MAXIMUM', 'Maximum', 'Maximum Mode'),
    ('ROUND', 'Round', 'Round Mode'),
    ('LESS_THAN', 'Less Than', 'Less Than Mode'),
    ('GREATER_THAN', 'Greater Than', 'Greater Than Mode'),
    ]

def get_nodes_links(context):
    space = context.space_data
    tree = space.node_tree
    nodes = tree.nodes
    links = tree.links
    active = nodes.active
    context_active = context.active_node
    # check if we are working on regular node tree or node group is currently edited.
    # if group is edited - active node of space_tree is the group
    # if context.active_node != space active node - it means that the group is being edited.
    # in such case we set "nodes" to be nodes of this group, "links" to be links of this group
    # if context.active_node == space.active_node it means that we are not currently editing group
    is_main_tree = True
    if active:
        is_main_tree = context_active == active
    if not is_main_tree:  # if group is currently edited
        tree = active.node_tree
        nodes = tree.nodes
        links = tree.links

    return nodes, links


class NWBase:
    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR' and space.node_tree is not None


class NWSwapNodeType(Operator, NWBase):
    """Swap type of selected nodes """
    bl_idname = "node.nw_swap_node_type"
    bl_label = "Swap Node Type"
    bl_options = {'REGISTER', 'UNDO'}
    
    to_type = EnumProperty(
        name="Swap to type",
        items=list(shaders_input_nodes_props) +\
            list(shaders_output_nodes_props) +\
            list(shaders_shader_nodes_props) +\
            list(shaders_texture_nodes_props) +\
            list(shaders_color_nodes_props) +\
            list(shaders_vector_nodes_props) +\
            list(shaders_converter_nodes_props) +\
            list(shaders_layout_nodes_props) +\
            list(compo_input_nodes_props) +\
            list(compo_output_nodes_props) +\
            list(compo_color_nodes_props) +\
            list(compo_converter_nodes_props) +\
            list(compo_filter_nodes_props) +\
            list(compo_vector_nodes_props) +\
            list(compo_matte_nodes_props) +\
            list(compo_distort_nodes_props) +\
            list(compo_layout_nodes_props),
        )
    
    def execute(self, context):
        nodes, links = get_nodes_links(context)
        to_type = self.to_type
        # Those types of nodes will not swap.
        src_excludes = ('NodeFrame')
        # Those attributes of nodes will be copied if possible
        attrs_to_pass = ('color', 'hide', 'label', 'mute', 'parent',\
            'show_options', 'show_preview', 'show_texture',\
            'use_alpha', 'use_clamp', 'use_custom_color', 'location'
            )
        selected = [n for n in nodes if n.select]
        reselect = []
        for node in [n for n in selected if\
                n.rna_type.identifier not in src_excludes and\
                n.rna_type.identifier != to_type]:
            new_node = nodes.new(to_type)
            for attr in attrs_to_pass:
                if hasattr(node, attr) and hasattr(new_node, attr):
                    setattr(new_node, attr, getattr(node, attr))
            # set image datablock of dst to image of src
            if hasattr(node, 'image') and hasattr(new_node, 'image'):
                if node.image:
                    new_node.image = node.image
            # Special cases
            if new_node.type == 'SWITCH':
                new_node.hide = True
            # Dictionaries: src_sockets and dst_sockets:
            # 'INPUTS': input sockets ordered by type (entry 'MAIN' main type of inputs).
            # 'OUTPUTS': output sockets ordered by type (entry 'MAIN' main type of outputs).
            # in 'INPUTS' and 'OUTPUTS':
            # 'SHADER', 'RGBA', 'VECTOR', 'VALUE' - sockets of those types.
            # socket entry:
            # (index_in_type, socket_index, socket_name, socket_default_value, socket_links)
            src_sockets = {
                'INPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
                'OUTPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
                }
            dst_sockets = {
                'INPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
                'OUTPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE': [], 'MAIN': None},
                }
            types_order_one = 'SHADER', 'RGBA', 'VECTOR', 'VALUE'
            types_order_two = 'SHADER', 'VECTOR', 'RGBA', 'VALUE'
            # check src node to set src_sockets values and dst node to set dst_sockets dict values
            for sockets, nd in ((src_sockets, node), (dst_sockets, new_node)):
                # Check node's inputs and outputs and fill proper entries in "sockets" dict
                for in_out, in_out_name in ((nd.inputs, 'INPUTS'), (nd.outputs, 'OUTPUTS')):
                    # enumerate in inputs, then in outputs
                    # find name, default value and links of socket
                    for i, socket in enumerate(in_out):
                        the_name = socket.name
                        dval = None
                        # Not every socket, especially in outputs has "default_value"
                        if hasattr(socket, 'default_value'):
                            dval = socket.default_value
                        socket_links = []
                        for lnk in socket.links:
                            socket_links.append(lnk)
                        # check type of socket to fill proper keys.
                        for the_type in types_order_one:
                            if socket.type == the_type:
                                # create values for sockets['INPUTS'][the_type] and sockets['OUTPUTS'][the_type]
                                # entry structure: (index_in_type, socket_index, socket_name, socket_default_value, socket_links)
                                sockets[in_out_name][the_type].append((len(sockets[in_out_name][the_type]), i, the_name, dval, socket_links))
                    # Check which of the types in inputs/outputs is considered to be "main".
                    # Set values of sockets['INPUTS']['MAIN'] and sockets['OUTPUTS']['MAIN']
                    for type_check in types_order_one:
                        if sockets[in_out_name][type_check]:
                            sockets[in_out_name]['MAIN'] = type_check
                            break
            
            matches = {
                    'INPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE_NAME': [], 'VALUE': [], 'MAIN': []},
                    'OUTPUTS': {'SHADER': [], 'RGBA': [], 'VECTOR': [], 'VALUE_NAME': [], 'VALUE': [], 'MAIN': []},
                    }
            
            for inout, soctype in (
                    ('INPUTS', 'MAIN',),
                    ('INPUTS', 'SHADER',),
                    ('INPUTS', 'RGBA',),
                    ('INPUTS', 'VECTOR',),
                    ('INPUTS', 'VALUE',),
                    ('OUTPUTS', 'MAIN',),
                    ('OUTPUTS', 'SHADER',),
                    ('OUTPUTS', 'RGBA',),
                    ('OUTPUTS', 'VECTOR',),
                    ('OUTPUTS', 'VALUE',),
                    ):
                if src_sockets[inout][soctype] and dst_sockets[inout][soctype]:
                    if soctype == 'MAIN':
                        sc = src_sockets[inout][src_sockets[inout]['MAIN']]
                        dt = dst_sockets[inout][dst_sockets[inout]['MAIN']]
                    else:
                        sc = src_sockets[inout][soctype]
                        dt = dst_sockets[inout][soctype]
                    # start with 'dt' to determine number of possibilities.
                    for i, soc in enumerate(dt):
                        # if src main has enough entries - match them with dst main sockets by indexes.
                        if len(sc) > i:
                            matches[inout][soctype].append(((sc[i][1], sc[i][3]), (soc[1], soc[3])))
                        # add 'VALUE_NAME' criterion to inputs.
                        if inout == 'INPUTS' and soctype == 'VALUE':
                            for s in sc:
                                if s[2] == soc[2]:  # if names match
                                    # append src (index, dval), dst (index, dval)
                                    matches['INPUTS']['VALUE_NAME'].append(((s[1], s[3]), (soc[1], soc[3])))
            
            # When src ['INPUTS']['MAIN'] is 'VECTOR' replace 'MAIN' with matches VECTOR if possible.
            # This creates better links when relinking textures.
            if src_sockets['INPUTS']['MAIN'] == 'VECTOR' and matches['INPUTS']['VECTOR']:
                matches['INPUTS']['MAIN'] = matches['INPUTS']['VECTOR']
            
            # Pass default values and RELINK:
            for tp in ('MAIN', 'SHADER', 'RGBA', 'VECTOR', 'VALUE_NAME', 'VALUE'):
                # INPUTS: Base on matches in proper order.
                for (src_i, src_dval), (dst_i, dst_dval) in matches['INPUTS'][tp]:
                    # pass dvals
                    if src_dval and dst_dval and tp in {'RGBA', 'VALUE_NAME'}:
                        new_node.inputs[dst_i].default_value = src_dval
                    # Special case: swap to math
                    if node.type in {'MIX_RGB', 'ALPHAOVER', 'ZCOMBINE'} and\
                            new_node.type == 'MATH' and\
                            tp == 'MAIN':
                        new_dst_dval = max(src_dval[0], src_dval[1], src_dval[2])
                        new_node.inputs[dst_i].default_value = new_dst_dval
                        if node.type == 'MIX_RGB':
                            if node.blend_type in [o[0] for o in operations]:
                                new_node.operation = node.blend_type
                    # Special case: swap from math to some types
                    if node.type == 'MATH' and\
                            new_node.type in {'MIX_RGB', 'ALPHAOVER', 'ZCOMBINE'} and\
                            tp == 'MAIN':
                        for i in range(3):
                            new_node.inputs[dst_i].default_value[i] = src_dval
                        if new_node.type == 'MIX_RGB':
                            if node.operation in [t[0] for t in blend_types]:
                                new_node.blend_type = node.operation
                            # Set Fac of MIX_RGB to 1.0
                            new_node.inputs[0].default_value = 1.0
                    # make link only when dst matching input is not linked already.
                    if node.inputs[src_i].links and not new_node.inputs[dst_i].links:
                        in_src_link = node.inputs[src_i].links[0]
                        in_dst_socket = new_node.inputs[dst_i]
                        links.new(in_src_link.from_socket, in_dst_socket)
                        links.remove(in_src_link)
                # OUTPUTS: Base on matches in proper order.
                for (src_i, src_dval), (dst_i, dst_dval) in matches['OUTPUTS'][tp]:
                    for out_src_link in node.outputs[src_i].links:
                        out_dst_socket = new_node.outputs[dst_i]
                        links.new(out_dst_socket, out_src_link.to_socket)
            # relink rest inputs if possible, no criteria
            for src_inp in node.inputs:
                for dst_inp in new_node.inputs:
                    if src_inp.links and not dst_inp.links:
                        src_link = src_inp.links[0]
                        links.new(src_link.from_socket, dst_inp)
                        links.remove(src_link)
            # relink rest outputs if possible, base on node kind if any left.
            for src_o in node.outputs:
                for out_src_link in src_o.links:
                    for dst_o in new_node.outputs:
                        if src_o.type == dst_o.type:
                            links.new(dst_o, out_src_link.to_socket)
            # relink rest outputs no criteria if any left. Link all from first output.
            for src_o in node.outputs:
                for out_src_link in src_o.links:
                    if new_node.outputs:
                        links.new(new_node.outputs[0], out_src_link.to_socket)
            nodes.remove(node)
        return {'FINISHED'}


###########################################
#
#   M E N U S
#
###########################################
class NWSwapNodeTypeMenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_node_type_menu"
    bl_label = "Swap Type to..."
    
    def draw(self, context):
        layout = self.layout
        tree = context.space_data.node_tree
        if tree.type == 'SHADER':
            layout.menu(NWSwapShadersInputSubmenu.bl_idname)
            layout.menu(NWSwapShadersOutputSubmenu.bl_idname)
            layout.menu(NWSwapShadersShaderSubmenu.bl_idname)
            layout.menu(NWSwapShadersTextureSubmenu.bl_idname)
            layout.menu(NWSwapShadersColorSubmenu.bl_idname)
            layout.menu(NWSwapShadersVectorSubmenu.bl_idname)
            layout.menu(NWSwapShadersConverterSubmenu.bl_idname)
            layout.menu(NWSwapShadersLayoutSubmenu.bl_idname)
        if tree.type == 'COMPOSITING':
            layout.menu(NWSwapCompoInputSubmenu.bl_idname)
            layout.menu(NWSwapCompoOutputSubmenu.bl_idname)
            layout.menu(NWSwapCompoColorSubmenu.bl_idname)
            layout.menu(NWSwapCompoConverterSubmenu.bl_idname)
            layout.menu(NWSwapCompoFilterSubmenu.bl_idname)
            layout.menu(NWSwapCompoVectorSubmenu.bl_idname)
            layout.menu(NWSwapCompoMatteSubmenu.bl_idname)
            layout.menu(NWSwapCompoDistortSubmenu.bl_idname)
            layout.menu(NWSwapCompoLayoutSubmenu.bl_idname)



class NWSwapShadersInputSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_input_submenu"
    bl_label = "Input"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_input_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersOutputSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_output_submenu"
    bl_label = "Output"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_output_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersShaderSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_shader_submenu"
    bl_label = "Shader"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_shader_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersTextureSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_texture_submenu"
    bl_label = "Texture"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_texture_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersColorSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_color_submenu"
    bl_label = "Color"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_color_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersVectorSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_vector_submenu"
    bl_label = "Vector"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_vector_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersConverterSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_converter_submenu"
    bl_label = "Converter"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_converter_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapShadersLayoutSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_shaders_layout_submenu"
    bl_label = "Layout"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in shaders_layout_nodes_props:
            if type != 'FRAME':
                props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
                props.to_type = ident

class NWSwapCompoInputSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_input_submenu"
    bl_label = "Input"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_input_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoOutputSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_output_submenu"
    bl_label = "Output"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_output_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoColorSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_color_submenu"
    bl_label = "Color"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_color_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoConverterSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_converter_submenu"
    bl_label = "Converter"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_converter_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoFilterSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_filter_submenu"
    bl_label = "Filter"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_filter_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoVectorSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_vector_submenu"
    bl_label = "Vector"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_vector_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoMatteSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_matte_submenu"
    bl_label = "Matte"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_matte_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoDistortSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_distort_submenu"
    bl_label = "Distort"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_distort_nodes_props:
            props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
            props.to_type = ident

class NWSwapCompoLayoutSubmenu(Menu, NWBase):
    bl_idname = "NODE_MT_nw_swap_compo_layout_submenu"
    bl_label = "Layout"
    
    def draw(self, context):
        layout = self.layout
        for ident, type, rna_name in compo_layout_nodes_props:
            if type != 'FRAME':
                props = layout.operator(NWSwapNodeType.bl_idname, text=rna_name)
                props.to_type = ident

addon_keymaps = []
# kmi_defs entry: (identifier, key, CTRL, SHIFT, ALT, props, nice name)
# props entry: (property name, property value)
kmi_defs = (
    ('wm.call_menu', 'S', True, True, True, (('name', NWSwapNodeTypeMenu.bl_idname),), "Swap node menu"),
    )

def register():
    bpy.utils.register_module(__name__)
    
    # keymaps
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Node Editor', space_type="NODE_EDITOR")
    for (identifier, key, CTRL, SHIFT, ALT, props, nicename) in kmi_defs:
        kmi = km.keymap_items.new(identifier, key, 'PRESS', ctrl=CTRL, shift=SHIFT, alt=ALT)
        if props:
            for prop, value in props:
                setattr(kmi.properties, prop, value)
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_module(__name__)
    
    # keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
