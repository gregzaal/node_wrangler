Todo
====

Short term:
-----------
* Merge NET type swapping
* Add driver for mapping node (option for offset) - drive the position, rotation and scale with an Empty
* Link Sky Texture vector with a Sun Lamp's rotation
* Color ramp element positions (node.color_ramp.elements[0])
* When viewing the image/mask/clip of a node, add button to header to jump back to node editor
* Add Vertex colors menu (same as UV Layers)
* Clamp the output of selected nodes (Mix node, second input, Clamp on)
* Improve panel layout
* Map Z-depth range by picking two points on the backdrop image (nearest, furthest), or by automatically mapping it so it's 0-1 (minimum 0, maximum 1)
* Ctrl+Shift+Click to cut lines and add clamps (not sure if this is possible with current api)
* Alt+Shift+Click to cut lines and add mix nodes

Long Term:
----------
* Tools for object/material index (both shading and compositing noodles, and for assigning)
* Node templates (store selection, new menu in Shift+A menu, new panel in toolbar) [something like this exists already? where?]
* Better auto-arrange that uses the starting position of nodes and centers them nicely rather than a long row at the top and ugly vertical 'columns'
