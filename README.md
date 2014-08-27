Node Wrangler
=============

**This repository is no longer up-to-date!**

The most recent version of this add-on can always be found [here](http://git.blender.org/gitweb/gitweb.cgi/blender-addons.git/blob_plain/HEAD:/node_efficiency_tools.py), in Blender's source code :) Which means you probably already have it installed and just need to [enable it](http://wiki.blender.org/index.php/Doc:2.6/Manual/Preferences/Addons) in your [User Preferences](http://wiki.blender.org/index.php/Doc:2.6/Manual/Preferences).

----

A Blender Addon with various tools to help node workflow.

Documentation: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Nodes/Nodes_Efficiency_Tools

Features
--------

* Viewer node for Cycles materials (Ctrl+Shift+Click)
* Delete unused nodes (Alt+X)
* UV Layer nodes - add an attribute node from a list of available UV maps with the name field already filled in (Shift+A > Input > UV Maps > [map name])
* Switch the type of one or more nodes to a related type, like a different shader (Alt+S), keeping inputs and outputs connected
* Swap the output connections of two nodes (Alt+Shift+S)
* Reset the compositor backdrop image zoom and position (Z)
* Frame the selected nodes (Shift+P)
* Reload the images of all the image nodes in the current tree (Alt+R)
* Quickly jump to the Image Editor and view the image of the selected node. Works for textures, movie clips, environment images, render layers, viewer nodes and masks.
* Automatically arrange the selected nodes (or all of them) in a non-overlapping linear layout (Q)