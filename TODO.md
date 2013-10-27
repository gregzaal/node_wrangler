Todo
====

Short term:
-----------
* Improve NET texture setup (Ctrl+T on texture nodes to add setup; fix mapping node size; add mapping between coord and texture)
* Improve NET Merge nodes (preference not to Hide node; place in center with dimensions)
* Merge NET type swapping
* Add driver for mapping node (option for offset) - drive the position, rotation and scale with an Empty
* Link Sky Texture vector with a Sun Lamp's rotation
* Color ramp element positions (node.color_ramp.elements[0])
* When viewing the image/mask/clip of a node, add button to header to jump back to node editor
* Add Vertex colors menu (same as UV Layers)
* Check for existance of UV layers or vert cols before appending to the menu
* Show a list of hotkeys in user prefs (in expandable box)
* Clamp the output of selected nodes (Mix node, second input, Clamp on)
* Add user preferences for stuff
    - Merge nodes position (lowest or middle)
    - Hide or Show Mix node when added
    - Antialias BGL lines (might cause issues for some cards, disable by default)
    - Precise laziness (don't use nearest node, but rather the exact node under the mouse (can't imagine why someone might want this, but good to have just in case))
    - Show a list of hokeys (not technically a user-preference, but it's a nice out-of-the-way place to put such a list)
* Improve panel layout
* In interactive mix and lazy connect, highlight the two nodes in real time (poke lukas_t about python access to node-space mouse coords and region-space node coords)
* When calculating nearest node, use nearest border, not nearest center
* Map Z-depth range by picking two points on the backdrop image (nearest, furthest), or by automatically mapping it so it's 0-1 (minimum 0, maximum 1)

Long Term:
----------
* Tools for object/material index (both shading and compositing noodles, and for assigning)
* Node templates (store selection, new menu in Shift+A menu, new panel in toolbar) [something like this exists already? where?]
* Better auto-arrange that uses the starting position of nodes and centers them nicely rather than a long row at the top and ugly vertical 'columns'
