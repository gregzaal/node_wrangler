Node Wrangler
=============
A Blender Addon with various tools to help node workflow.

Download latest version: https://raw.github.com/gregzaal/node_wrangler/master/node_wrangler.py (right click > Save link as...)

Documentation for version 1.0: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Nodes/Node_Wrangler
Current version: 2.0

Features
--------

New to 2.0:
    Material Viewer Node (Ctrl+Shift+Click) Connects a node to a temporary Emission shader as a dummy Viewer node to quickly see what the output of a node looks like. Emission strength matches Film Exposure so that colours are never over/under bright. If Ctrl+Shift+Clicking on a shader node, connect that to the material output and remove the dummy Viewer.
    UV layer nodes (Add > Input > UV Maps > [uv name]) a list of all uv layers on all objects with this material, adds an Attribute node with the name already filled in.
    Type swapping (Alt+S): Change the type of selected nodes (either shaders or textures) to a similar type (eg. shader type), keeping inputs and outputs connected
    Output Swapping (Alt+Shift+S): Exchange two node's output connections
    Removed backdrop Zoom-Fit (now in trunk as alt+Home)
    Reset backdrop zoom and position with Z
    Frame the selected nodes with Shift+P (adds frame node, parents selection to it)