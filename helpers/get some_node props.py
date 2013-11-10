# HELPER
# This script helps creating lists of properties of nodes.
# Creating variables that store several nodes' properties that will then be used to add new nodes, change nodes' types etc.
# may be a time consuming process where you go through several data by hand and try to figure out how certain things are named.
# I used this little script to create "swap_submenu_items.py" file.
#
#
#
##############################
#
# WORKFLOW
#
# 1. create variable's name and set it to tuple type
# 2. Create text datablock named 'storage'
# 3. Add node from "ADD NODE" menu (one by one for every type of node from every "category")
# 4. run script.
#
# this will create new line in the 'storage' text datablock.
#
# 5. When completing with all submenu items, we can copy lines of 'storage' and paste to entries of variable.
#
#
#
# Just take a look at the script and you'll figure out other uses of it.

import bpy

nodes = bpy.context.scene.node_tree.nodes

n = nodes.active

the_string = "    ('" + n.rna_type.identifier + "', '" + n.type + "', '" + n.rna_type.name + "'),\n"
bpy.data.texts['storage'].write(the_string)
print(the_string)