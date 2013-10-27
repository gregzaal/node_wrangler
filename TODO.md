Todo
====

Short term:
-----------
* Improve NET Merge nodes (preference not to Hide node; place in center with dimensions)
* Merge NET type swapping
* Add driver for mapping node (option for offset) - drive the position, rotation and scale with an Empty
* Link Sky Texture vector with a Sun Lamp's rotation
* Color ramp element positions (node.color_ramp.elements[0])
* When viewing the image/mask/clip of a node, add button to header to jump back to node editor
* Add Vertex colors menu (same as UV Layers)
* Clamp the output of selected nodes (Mix node, second input, Clamp on)
* Add user preferences for stuff
    - Merge nodes position (lowest or middle)
* Improve panel layout
* In interactive mix and lazy connect, highlight the two nodes in real time (poke lukas_t about python access to node-space mouse coords and region-space node coords)
* Map Z-depth range by picking two points on the backdrop image (nearest, furthest), or by automatically mapping it so it's 0-1 (minimum 0, maximum 1)

Long Term:
----------
* Tools for object/material index (both shading and compositing noodles, and for assigning)
* Node templates (store selection, new menu in Shift+A menu, new panel in toolbar) [something like this exists already? where?]
* Better auto-arrange that uses the starting position of nodes and centers them nicely rather than a long row at the top and ugly vertical 'columns'
