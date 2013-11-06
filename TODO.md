Todo
====

Short term:
-----------
* BUG: Arrange Nodes does not use selection?
* Add driver for mapping node (option for offset) - drive the position, rotation and scale with an Empty
* Link Sky Texture vector with a Sun Lamp's rotation
* Color ramp element positions (node.color_ramp.elements[0])
* Add Vertex colors menu (same as UV Layers)
* Clamp the output of selected nodes (Mix node, second input, Clamp on)
* Map Z-depth range by picking two points on the backdrop image (nearest, furthest), or by automatically mapping it so it's 0-1 (minimum 0, maximum 1)
* Ctrl+Shift+Click to cut lines and add clamps (not sure if this is possible with current api)
* Alt+Shift+Click to cut lines and add mix nodes
* Comment node
 - Multiline
 - Automatic wordwrap
 - No character limit
 - Heading
 - Text colour
 - Use frame node and parent text to this
* Add "Are you sure" dialog for Delete Unused Nodes
* Hotkey for 'View Image' function
* Save Image - similar to View Image, but now just for saving
* When viewing the image/mask/clip of a node, add button to header to jump back to node editor
* Show current frame number at bottom right of node editor (user preference)
* Auto set frame range of image sequence
* Make sure everything works inside groups.
* Make Lazy Connect replace other links when theres no free one available.
* Add hack_force_update call to lazy mix and output swap

Long Term:
----------
* Tools for object/material index (both shading and compositing noodles, and for assigning)
* Node templates (store selection, new menu in Shift+A menu, new panel in toolbar) [Amaranth has one template, but only one, might like to look at this code]
* Better auto-arrange that uses the starting position of nodes and centers them nicely rather than a long row at the top and ugly vertical 'columns'
* Set Camera clipping automatically (fire rays into scene progressively, show user real-time the min/max, have 'stop' button to cancel early and use those values, or stop after a certain number of rays). Also allow user to click the model in camera view to set closest/furthest. Include bgl visualisation of the progressive points, and bgl camera view borders (shown in non-camera persp)
