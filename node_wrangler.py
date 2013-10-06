# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Node Wrangler",
    "author": "Greg Zaal",
    "version": (2, 0),
    "blender": (2, 68, 2),
    "location": "Node Editor > Z key/Q key or Properties Region",
    "description": "A set of tools that help clean up a node tree and improve viewing usability.",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php?title=Extensions:2.6/Py/Scripts/Nodes/Node_Wrangler",
    "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=35786&group_id=153&atid=467",
    "category": "Node"}

import bpy
from collections import Counter as counter
from mathutils import Vector


'''
TODO:
    More swapping types?
'''

shader_list = [['ShaderNodeBsdfTransparent', 'BSDF_TRANSPARENT', 'Transparent'],
               ['ShaderNodeBsdfGlossy', 'BSDF_GLOSSY', 'Glossy'],
               ['ShaderNodeBsdfGlass', 'BSDF_GLASS', 'Glass'],
               ['ShaderNodeBsdfDiffuse', 'BSDF_DIFFUSE', 'Diffuse'],
               ['ShaderNodeSubsurfaceScattering', 'SUBSURFACE_SCATTERING', 'SSS'],
               ['ShaderNodeEmission', 'EMISSION', 'Emission'],
               ['ShaderNodeBsdfVelvet', 'BSDF_VELVET', 'Velvet'],
               ['ShaderNodeBsdfTranslucent', 'BSDF_TRANSLUCENT', 'Translucent'],
               ['ShaderNodeAmbientOcclusion', 'AMBIENT_OCCLUSION', 'AO'],
               ['ShaderNodeBackground', 'BACKGROUND', 'Background'],
               ['ShaderNodeBsdfRefraction', 'BSDF_REFRACTION', 'Refraction'],
               ['ShaderNodeBsdfAnisotropic', 'BSDF_ANISOTROPIC', 'Anisotropic'],
               ['ShaderNodeHoldout', 'HOLDOUT', 'Holdout']]
shader_idents = list(x[0] for x in shader_list)
shader_types = list(x[1] for x in shader_list)
shader_names = list(x[2] for x in shader_list)

texture_list = [['ShaderNodeTexImage', 'TEX_IMAGE', 'Image'],
                ['ShaderNodeTexEnvironment', 'TEX_ENVIRONMENT', 'Environment'],
                ['ShaderNodeTexSky', 'TEX_SKY', 'Sky'],
                ['ShaderNodeTexNoise', 'TEX_NOISE', 'Noise'],
                ['ShaderNodeTexWave', 'TEX_WAVE', 'Wave'],
                ['ShaderNodeTexVoronoi', 'TEX_VORONOI', 'Voronoi'],
                ['ShaderNodeTexMusgrave', 'TEX_MUSGRAVE', 'Musgrave'],
                ['ShaderNodeTexGradient', 'TEX_GRADIENT', 'Gradient'],
                ['ShaderNodeTexMagic', 'TEX_MAGIC', 'Magic'],
                ['ShaderNodeTexChecker', 'TEX_CHECKER', 'Checker'],
                ['ShaderNodeTexBrick', 'TEX_BRICK', 'Brick']]
texture_idents = list(x[0] for x in texture_list)
texture_types = list(x[1] for x in texture_list)
texture_names = list(x[2] for x in texture_list)

mix_shader_types = ['MIX_SHADER', 'ADD_SHADER']
output_types = ['OUTPUT_MATERIAL', 'OUTPUT_WORLD', 'OUTPUT_LAMP', 'COMPOSITE']


def get_nodes_links_withsel(context):  # Taken from Node Efficiency Tools by Bartek Skorupa (link at bottom)
    space = context.space_data
    tree = space.node_tree
    nodes = tree.nodes
    links = tree.links
    active = nodes.active
    context_active = context.active_node
    is_main_tree = True
    if active:
        is_main_tree = context_active == active
    if not is_main_tree:  # if group is currently edited
        tree = active.node_tree
        nodes = tree.nodes
        links = tree.links
    all_nodes = nodes
    newnodes = []   
    for node in nodes:
        if node.select == True:
            newnodes.append(node)
    if len(newnodes) == 0:
        newnodes = all_nodes
    nodes_sorted = sorted(newnodes, key=lambda x: x.name)               # Sort the nodes list to achieve consistent
    links_sorted = sorted(links, key=lambda x: x.from_node.name)   # results (order was changed based on selection).
    return nodes_sorted, links_sorted


def get_nodes_links(context):
    space = context.space_data
    tree = space.node_tree
    nodes = tree.nodes
    links = tree.links
    active = nodes.active
    context_active = context.active_node
    is_main_tree = True
    if active:
        is_main_tree = context_active == active
    if not is_main_tree:  # if group is currently edited
        tree = active.node_tree
        nodes = tree.nodes
        links = tree.links

    return nodes, links


def isStartNode(node):
    bool = True
    if len(node.inputs):
        for input in node.inputs:
            if input.links != ():
                bool = False
    return bool


def isEndNode(node):
    bool = True
    if len(node.outputs):
        for output in node.outputs:
            if output.links != ():
                bool = False
    return bool


def between(b1, a, b2):
    #   b1 MUST be smaller than b2!
    bool = False
    if a >= b1 and a <= b2:
        bool = True
    return bool


def overlaps(node1, node2):
    dim1x = node1.dimensions.x
    dim1y = node1.dimensions.y
    dim2x = node2.dimensions.x
    dim2y = node2.dimensions.y
    boolx = False
    booly = False
    boolboth = False

    # check for x overlap
    if between(node2.location.x, node1.location.x, (node2.location.x + dim2x)) or between(node2.location.x, (node1.location.x + dim1x), (node2.location.x + dim2x)):  # if either edges are inside the second node
        boolx = True
    if between(node1.location.x, node2.location.x, node1.location.x + dim1x) and between(node1.location.x, (node2.location.x + dim2x), node1.location.x + dim1x):  # if each edge is on either side of the second node
        boolx = True

    # check for y overlap
    if between((node2.location.y - dim2y), node1.location.y, node2.location.y) or between((node2.location.y - dim2y), (node1.location.y - dim1y), node2.location.y):
        booly = True
    if between((node1.location.y - dim1y), node2.location.y, node1.location.y) and between((node1.location.y - dim1y), (node2.location.y - dim2y), node1.location.y):
        booly = True

    if boolx == True and booly == True:
        boolboth = True
    return boolboth


def treeMidPt(nodes):
    minx = (sorted(nodes, key=lambda k: k.location.x))[0].location.x
    miny = (sorted(nodes, key=lambda k: k.location.y))[0].location.y
    maxx = (sorted(nodes, key=lambda k: k.location.x, reverse=True))[0].location.x
    maxy = (sorted(nodes, key=lambda k: k.location.y, reverse=True))[0].location.y

    midx = minx + ((maxx - minx) / 2)
    midy = miny + ((maxy - miny) / 2)

    return midx, midy


class LinkToOutputNode(bpy.types.Operator):  # Partially taken from Node Efficiency Tools by Bartek Skorupa
    bl_idname = "nw.link_out"
    bl_label = "Connect to Output"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        space = context.space_data
        return (space.type == 'NODE_EDITOR' and space.node_tree is not None and context.active_node is not None)
    
    def execute(self, context):
        nodes, links = get_nodes_links(context)
        active = nodes.active
        output_node = None
        tree_type = context.space_data.tree_type
        for node in nodes:
            if node.type in output_types:
                output_node = node
                break
        if not output_node:
            bpy.ops.node.select_all(action="DESELECT")
            if tree_type == 'ShaderNodeTree':
                output_node = nodes.new('ShaderNodeOutputMaterial')
            elif tree_type == 'CompositorNodeTree':
                output_node = nodes.new('CompositorNodeComposite')
            output_node.location.x = active.location.x + active.dimensions.x + 80
            output_node.location.y = active.location.y
        if (output_node and active.outputs):
            output_index = 0
            for i, output in enumerate(active.outputs):
                if output.type == output_node.inputs[0].type:
                    output_index = i
                    break

            out_input_index = 0
            if tree_type == 'ShaderNodeTree':
                if active.outputs[output_index].type != 'SHADER': # connect to displacement if not a shader
                    out_input_index = 2
            links.new(active.outputs[output_index], output_node.inputs[out_input_index])

        return {'FINISHED'}


class ArrangeNodes(bpy.types.Operator):

    'Automatically layout the selected nodes in a linear and non-overlapping fashion.'
    bl_idname = 'nw.layout'
    bl_label = 'Arrange Nodes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        nodes, links = get_nodes_links_withsel(context)
        margin = context.scene.Spacing

        oldmidx, oldmidy = treeMidPt(nodes)

        if context.scene.DelReroutes:
            # Store selection
            selection = []
            for node in nodes:
                if node.select == True and node.type != "REROUTE":
                    selection.append(node.name)
            # Delete Reroutes
            for node in nodes:
                node.select = False  # deselect all nodes
            for node in nodes:
                if node.type == 'REROUTE':
                    node.select = True
                    bpy.ops.node.delete_reconnect()
            # Restore selection
            #nodes, links = get_nodes_links(context)
            for node in nodes:
                if node.name in selection:
                    node.select = True
        else:
            # Store selection anyway
            selection = []
            for node in nodes:
                if node.select == True:
                    selection.append(node.name)

        if context.scene.FrameHandling == "delete":
            # Store selection
            selection = []
            for node in nodes:
                if node.select == True and node.type != "FRAME":
                    selection.append(node.name)
            # Delete Frames
            for node in nodes:
                node.select = False  # deselect all nodes
            for node in nodes:
                if node.type == 'FRAME':
                    node.select = True
                    bpy.ops.node.delete()
            # Restore selection
            #nodes, links = get_nodes_links(context)
            for node in nodes:
                if node.name in selection:
                    node.select = True

        layout_iterations = len(nodes)*2
        for it in range(0, layout_iterations):
            for node in nodes:
                isframe = False
                if node.type == "FRAME" and context.scene.FrameHandling == 'ignore':
                    isframe = True
                if not isframe:
                    if isStartNode(node) and context.scene.StartAlign:  # line up start nodes
                        node.location.x = node.dimensions.x / -2
                        node.location.y = node.dimensions.y / 2
                    for link in links:
                        if link.from_node == node and link.to_node in nodes:
                            link.to_node.location.x = node.location.x + node.dimensions.x + margin
                            link.to_node.location.y = node.location.y - (node.dimensions.y / 2) + (link.to_node.dimensions.y / 2)
                else:
                    node.location.x = 0
                    node.location.y = 0

        backward_check_iterations = len(nodes)
        for it in range(0, backward_check_iterations):
            for link in links:
                if link.from_node.location.x + link.from_node.dimensions.x >= link.to_node.location.x and link.to_node in nodes:
                    link.to_node.location.x = link.from_node.location.x + link.from_node.dimensions.x + margin

        # line up end nodes
        if context.scene.EndAlign:
            for node in nodes:
                max_loc_x = (sorted(nodes, key=lambda x: x.location.x, reverse=True))[0].location.x
                if isEndNode(node) and not isStartNode(node):
                    node.location.x = max_loc_x

        overlap_iterations = len(nodes)
        for it in range(0, overlap_iterations):
            for node in nodes:
                isframe = False
                if node.type == "FRAME" and context.scene.FrameHandling == 'ignore':
                    isframe = True
                if not isframe:
                    for nodecheck in nodes:
                        isframe = False
                        if nodecheck.type == "FRAME" and context.scene.FrameHandling == 'ignore':
                            isframe = True
                        if not isframe:
                            if (node != nodecheck):  # dont look for overlaps with self
                                if overlaps(node, nodecheck):
                                    node.location.y = nodecheck.location.y - nodecheck.dimensions.y - 0.5 * margin

        newmidx, newmidy = treeMidPt(nodes)
        middiffx = newmidx - oldmidx
        middiffy = newmidy - oldmidy

        # put nodes back to the center of the old center
        for node in nodes:
            node.location.x = node.location.x - middiffx
            node.location.y = node.location.y - middiffy

        return {'FINISHED'}


class DeleteUnusedNodes(bpy.types.Operator):

    'Delete all nodes whose output is not used'
    bl_idname = 'nw.del_unused'
    bl_label = 'Delete Unused Nodes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        end_types = ['OUTPUT_MATERIAL', 'OUTPUT', 'VIEWER', 'COMPOSITE', 'SPLITVIEWER', 'OUTPUT_FILE', 'LEVELS', 'OUTPUT_LAMP', 'OUTPUT_WORLD', 'GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT']

        # Store selection
        selection = []
        for node in nodes:
            if node.select == True:
                selection.append(node.name)

        deleted_nodes = []
        temp_deleted_nodes = []
        del_unused_iterations = len(nodes)
        for it in range(0, del_unused_iterations):
            temp_deleted_nodes = list(deleted_nodes) # keep record of last iteration
            for node in nodes:
                node.select = False
            for node in nodes:
                if isEndNode(node) and not node.type in end_types:
                    node.select = True
                    deleted_nodes.append(node.name)
                    bpy.ops.node.delete()

            if temp_deleted_nodes == deleted_nodes: # stop iterations when there are no more nodes to be deleted
                break

        deleted_nodes = list(set(deleted_nodes))  # get unique list of deleted nodes (iterations would count the same node more than once)
        for n in deleted_nodes:
            self.report({'INFO'}, "Node " + n + " deleted")
        num_deleted = len(deleted_nodes)
        n=' node'
        if num_deleted>1:
            n+='s'
        if num_deleted:
            self.report({'INFO'}, "Deleted " + str(num_deleted) + n)
        else:
            self.report({'INFO'}, "Nothing deleted")

        # Restore selection
        nodes, links = get_nodes_links(context)
        for node in nodes:
            if node.name in selection:
                node.select = True
        return {'FINISHED'}


class NWResetBG(bpy.types.Operator):

    'Reset the zoom and position of the background image'
    bl_idname = 'nw.bg_reset'
    bl_label = 'Reset Backdrop'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        snode = context.space_data
        return snode.tree_type == 'CompositorNodeTree'

    def execute(self, context):
        context.space_data.backdrop_zoom = 1
        context.space_data.backdrop_x = 0
        context.space_data.backdrop_y = 0
        return {'FINISHED'}


class NWSwapOutputs(bpy.types.Operator):

    "Swap the output connections of the two selected nodes"
    bl_idname = 'nw.swap_outputs'
    bl_label = 'Swap Outputs'
    newtype = bpy.props.StringProperty()
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        snode = context.space_data
        return len(context.selected_nodes) == 2

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        selected_nodes = context.selected_nodes
        n1 = selected_nodes[0]
        n2 = selected_nodes[1]
        n1_outputs = []
        n2_outputs = []

        out_index = 0
        for output in n1.outputs:
            if output.links:
                for link in output.links:
                    n1_outputs.append([out_index, link.to_socket])
                    links.remove(link)
            out_index += 1

        out_index = 0
        for output in n2.outputs:
            if output.links:
                for link in output.links:
                    n2_outputs.append([out_index, link.to_socket])
                    links.remove(link)
            out_index += 1

        for connection in n1_outputs:
            try:
                links.new(n2.outputs[connection[0]], connection[1])
            except:
                self.report({'WARNING'}, "Some connections have been lost due to differing numbers of output sockets")
        for connection in n2_outputs:
            try:
                links.new(n1.outputs[connection[0]], connection[1])
            except:
                self.report({'WARNING'}, "Some connections have been lost due to differing numbers of output sockets")

        return {'FINISHED'}


class NWSwapType(bpy.types.Operator):

    "Swap the selected nodes to another type"
    bl_idname = 'nw.swap'
    bl_label = 'Swap Type'
    newtype = bpy.props.StringProperty()
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        nodes, links = get_nodes_links(context)

        selected_nodes = context.selected_nodes
        new_nodes = []
        for node in selected_nodes:
            # connections list: to/from socket object, swapped node's socket name, swapped node's socket type
            input_connections = []
            output_connections = []
            newnode = nodes.new(self.newtype)
            newnode.location.x = node.location.x
            newnode.location.y = node.location.y

            for inpt in node.inputs:
                for link in inpt.links:
                    input_connections.append((link.from_socket, link.to_socket.name, link.to_socket.type))
            for c in input_connections:
                connection_made = False
                for inpt in newnode.inputs:
                    if inpt.name == c[1] and not connection_made:
                        links.new(c[0], inpt)
                        connection_made = True
                if not connection_made: # if there is no socket name match, try to match by type
                    for inpt in newnode.inputs:
                        if inpt.type == c[2] and not connection_made:
                            links.new(c[0], inpt)
                            connection_made = True

            for outpt in node.outputs:
                for link in outpt.links:
                    output_connections.append((link.to_socket, link.from_socket.name, link.from_socket.type))
            for c in output_connections:
                connection_made = False
                for outpt in newnode.outputs:
                    if outpt.name == c[1] and not connection_made:
                        links.new(c[0], outpt)
                        connection_made = True
                if not connection_made:
                    for outpt in newnode.outputs:
                        if outpt.type == c[2] and not connection_made:
                            links.new(c[0], outpt)
                            connection_made = True

            newnode.select = False
            new_nodes.append(newnode)

        bpy.ops.node.delete() # remove old nodes

        for n in new_nodes:
            n.select = True

        return {'FINISHED'}


class NWSwapMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_type_swap_menu"
    bl_label = "Swap the type of selected nodes"

    @classmethod
    def poll(cls, context):
        if context.area.spaces[0].node_tree:
            if context.area.spaces[0].node_tree.type == 'SHADER':
                if len(list(x for x in context.area.spaces[0].node_tree.nodes if x.select == True)) > 0: # if any nodes are selected
                    selected_types = list(k.type for k in context.area.spaces[0].node_tree.nodes if k.select == True)
                    if list(x for x in selected_types if x in shader_types) or list(x for x in selected_types if x in texture_types):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
            
    def draw(self, context):
        l = self.layout
        nodes, links = get_nodes_links(context)

        selected_types = list(k.type for k in nodes if k.select == True)

        swap_type=''
        if list(x for x in selected_types if x in shader_types):
            swap_type += 'shader'
        if list(x for x in selected_types if x in texture_types):
            swap_type += 'texture'

        index=0
        if 'shader' in swap_type:
            for node_type in shader_names:
                l.operator("nw.swap", text = node_type).newtype = shader_idents[index]
                index+=1
            if 'shader' != swap_type:
                l.separator()
                index = 0
        if 'texture' in swap_type:
            for node_type in texture_names:
                l.operator("nw.swap", text = node_type).newtype = texture_idents[index]
                index+=1


class NWAddUVNode(bpy.types.Operator):

    "Add an Attribute node for this UV layer"
    bl_idname = 'nw.add_uv_node'
    bl_label = 'Add UV map'
    uv_name = bpy.props.StringProperty()
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.node.add_node('INVOKE_DEFAULT', use_transform=True, type="ShaderNodeAttribute")
        nodes, links = get_nodes_links(context)
        nodes.active.attribute_name = self.uv_name
        return {'FINISHED'}


class NWUVMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_node_uvs_menu"
    bl_label = "UV Maps"

    @classmethod
    def poll(cls, context):
        if context.area.spaces[0].node_tree:
            if context.area.spaces[0].node_tree.type == 'SHADER':
                return True
            else:
                return False
        else:
            return False
            
    def draw(self, context):
        l = self.layout
        nodes, links = get_nodes_links(context)
        mat = context.object.active_material

        objs = []
        for obj in bpy.data.objects:
            for slot in obj.material_slots:
                if slot.material == mat:
                    objs.append(obj)
        uvs = []
        for obj in objs:
            if obj.data.uv_layers:
                for uv in obj.data.uv_layers:
                    uvs.append(uv.name)
        uvs = list(set(uvs)) # get a unique list

        if uvs:
            for uv in uvs:
                l.operator('nw.add_uv_node', text = uv).uv_name = uv
        else:
            l.label("No UV layers on objects with this material")


class NWEmissionViewer(bpy.types.Operator):
    bl_idname = "nw.emission_viewer"
    bl_label = "Emission Viewer"
    bl_description = "Connect active node to Emission Shader for shadeless previews"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space = context.space_data
        valid = False
        if space.type == 'NODE_EDITOR':
            #if space.tree_type == 'ShaderNodeTree' and space.node_tree is not None and context.active_node is not None and context.active_node.type != "OUTPUT_MATERIAL":
            if space.tree_type == 'ShaderNodeTree' and space.node_tree is not None and context.active_node.type != "OUTPUT_MATERIAL":
                valid = True
        return valid

    def invoke(self, context, event):
    #def execute(self, context):

        # to select at specific mouse position:
        # bpy.ops.node.select(mouse_x=156, mouse_y=410, extend=False)

        mlocx = event.mouse_region_x
        mlocy = event.mouse_region_y
        select_node = bpy.ops.node.select(mouse_x=mlocx, mouse_y=mlocy, extend=False)
        if 'FINISHED' in select_node: # only run if mouse click is on a node
            nodes, links = get_nodes_links(context)
            active = nodes.active
            valid = False
            if active:
                if active.select:
                    if active.type not in shader_types and active.type not in mix_shader_types:
                        valid = True
            if valid:                        
                # get material_output node
                materialout_exists=False
                materialout=None # placeholder node
                for node in nodes:
                    if node.type=="OUTPUT_MATERIAL":
                        materialout_exists=True
                        materialout=node
                if not materialout:
                    materialout = nodes.new('ShaderNodeOutputMaterial')
                    sorted_by_xloc = (sorted(nodes, key=lambda x: x.location.x))
                    max_xloc_node = sorted_by_xloc[-1]
                    if max_xloc_node.name == 'Emission Viewer':
                        max_xloc_node = sorted_by_xloc[-2]
                    materialout.location.x = max_xloc_node.location.x + max_xloc_node.dimensions.x + 80
                    sum_yloc = 0
                    for node in nodes:
                        sum_yloc += node.location.y
                    materialout.location.y = sum_yloc/len(nodes) #put material output at average y location
                    materialout.select=False
                # get Emission Viewer node
                emission_exists=False
                emission_placeholder=nodes[0]
                for node in nodes:
                    if "Emission Viewer" in node.name:
                        emission_exists=True
                        emission_placeholder=node
                        
                position=0
                for link in links: # check if Emission Viewer is already connected to active node
                    if link.from_node.name==active.name and "Emission Viewer" in link.to_node.name and "Emission Viewer" in materialout.inputs[0].links[0].from_node.name:
                        num_outputs=len(link.from_node.outputs)
                        index=0
                        for output in link.from_node.outputs:
                            if link.from_socket==output:
                                position=index
                            index=index+1
                        position=position+1
                        if position>=num_outputs:
                            position=0
                            
                # Store selection
                selection=[]
                for node in nodes:
                   if node.select==True:
                        selection.append(node.name)       
                
                locx = active.location.x
                locy = active.location.y
                dimx = active.dimensions.x
                dimy = active.dimensions.y
                if not emission_exists:
                    emission = nodes.new('ShaderNodeEmission')
                    emission.hide=True
                    emission.location = [materialout.location.x, (materialout.location.y+40)]
                    emission.label="Viewer"
                    emission.name="Emission Viewer"
                    emission.use_custom_color=True
                    emission.color=(0.6,0.5,0.4)
                else:
                    emission=emission_placeholder
                           
                nodes.active = emission
                links.new(active.outputs[position], emission.inputs[0])
                bpy.ops.nw.link_out()
                    
                # Restore selection
                emission.select=False
                nodes.active=active
                for node in nodes:
                    if node.name in selection:
                        node.select=True 
            else: # if active node is a shader, connect to output
                try:
                    bpy.ops.nw.link_out()
                except:
                    self.report({'ERROR'}, "Shader viewing relies on a function of the Node Efficiency Tools addon") # for now!
                finally:
                    # ----Delete Emission Viewer----            
                    if len(list(x for x in nodes if x.name == 'Emission Viewer')) > 0:
                        # Store selection
                        selection=[]
                        for node in nodes:
                           if node.select==True:
                                selection.append(node.name)
                                node.select=False
                        # Delete it
                        nodes['Emission Viewer'].select = True
                        bpy.ops.node.delete()
                        # Restore selection
                        for node in nodes:
                            if node.name in selection:
                                node.select=True 

            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class NWFrameSelected(bpy.types.Operator):
    bl_idname = "nw.frame_selected"
    bl_label = "Frame Selected"
    bl_description = "Add a frame node and parent the selected nodes to it"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        space = context.space_data
        valid = False
        if space.type == 'NODE_EDITOR':
            if space.node_tree is not None:
                valid = True
        return valid

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        selected = []
        for node in nodes:
            if node.select==True:
                selected.append(node)
                
        bpy.ops.node.add_node(type='NodeFrame')
        frm=nodes.active
        
        for node in selected:
            node.parent=frm

        return {'FINISHED'}


class NodeWranglerPanel(bpy.types.Panel):
    bl_idname = "NODE_PT_node_wrangler"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = "Node Wrangler"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        col = box.column(align=True)
        col.operator("nw.layout", icon="IMGDISPLAY")
        col.prop(scene, "StartAlign")
        col.prop(scene, "EndAlign")
        col.prop(scene, "DelReroutes")
        col.prop(scene, "FrameHandling")
        col.separator()
        col.prop(scene, "Spacing")
        col = layout.column(align=True)
        col.operator("nw.del_unused", icon="CANCEL", text="Delete Unused Nodes")
        col.operator("nw.frame_selected", icon="MENU_PANEL")


def uvs_menu_func(self, context):
    self.layout.menu("NODE_MT_node_uvs_menu")


def bgreset_menu_func(self, context):
    self.layout.operator("nw.bg_reset")


addon_keymaps = []


def register():
    # props
    bpy.types.Scene.StartAlign = bpy.props.BoolProperty(
        name="Align Start Nodes",
        default=True,
        description="Put all nodes with no inputs on the left of the tree")
    bpy.types.Scene.EndAlign = bpy.props.BoolProperty(
        name="Align End Nodes",
        default=True,
        description="Put all nodes with no outputs on the right of the tree")
    bpy.types.Scene.Spacing = bpy.props.FloatProperty(
        name="Spacing",
        default=80.0,
        min=0.0,
        description="The horizonal space between nodes (vertical is half this)")
    bpy.types.Scene.DelReroutes = bpy.props.BoolProperty(
        name="Delete Reroutes",
        default=True,
        description="Delete all Reroute nodes to avoid unexpected layouts")
    bpy.types.Scene.FrameHandling = bpy.props.EnumProperty(
        name="Frames",
        items=(("ignore", "Ignore", "Do nothing about Frame nodes (can be messy)"), ("delete", "Delete", "Delete Frame nodes")),
        default='ignore',
        description="How to handle Frame nodes")

    bpy.utils.register_module(__name__)

    bpy.types.NODE_MT_category_SH_NEW_INPUT.append(uvs_menu_func)
    bpy.types.NODE_PT_backdrop.append(bgreset_menu_func)

    # add keymap entry
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
    kmi = km.keymap_items.new("nw.bg_reset", 'Z', 'PRESS')
    kmi = km.keymap_items.new("nw.layout", 'Q', 'PRESS')
    kmi = km.keymap_items.new("nw.del_unused", 'X', 'PRESS', alt=True)
    kmi = km.keymap_items.new("nw.frame_selected", 'P', 'PRESS', shift=True)
    kmi = km.keymap_items.new("nw.emission_viewer", 'LEFTMOUSE', 'PRESS', ctrl=True, shift=True)
    kmi = km.keymap_items.new("nw.swap_outputs", 'S', 'PRESS', alt=True, shift=True)
    km.keymap_items.new("wm.call_menu", 'S', 'PRESS', alt=True).properties.name='NODE_MT_type_swap_menu'

    addon_keymaps.append(km)


def unregister():
    # props
    del bpy.types.Scene.StartAlign
    del bpy.types.Scene.EndAlign
    del bpy.types.Scene.Spacing
    del bpy.types.Scene.DelReroutes
    del bpy.types.Scene.FrameHandling

    bpy.utils.unregister_module(__name__)

    bpy.types.NODE_MT_category_SH_NEW_INPUT.remove(uvs_menu_func)
    bpy.types.NODE_PT_backdrop.remove(bgreset_menu_func)

    # remove keymap entry
    for km in addon_keymaps:
        bpy.context.window_manager.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()

'''
A small portion of this code (marked by a comment in the function definition) was taken from Bartek Skorupa's "Node
Efficiency Tools" GPL addon (http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Nodes/Nodes_Efficiency_Tools)
'''