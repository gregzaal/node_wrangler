# shader nodes
shaders_input_submenu_items = (
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
shaders_output_submenu_items = (
    ('ShaderNodeOutputMaterial', 'OUTPUT_MATERIAL', 'Material Output'),
    ('ShaderNodeOutputLamp', 'OUTPUT_LAMP', 'Lamp Output'),
    ('ShaderNodeOutputWorld', 'OUTPUT_WORLD', 'World Output'),
    )
shaders_shader_submenu_items = (
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
shaders_texture_submenu_items = (
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
shaders_color_submenu_items(
    ('ShaderNodeMixRGB', 'MIX_RGB', 'MixRGB'),
    ('ShaderNodeRGBCurve', 'CURVE_RGB', 'RGB Curves'),
    ('ShaderNodeInvert', 'INVERT', 'Invert'),
    ('ShaderNodeLightFalloff', 'LIGHT_FALLOFF', 'Light Falloff'),
    ('ShaderNodeHueSaturation', 'HUE_SAT', 'Hue/Saturation'),
    ('ShaderNodeGamma', 'GAMMA', 'Gamma'),
    ('ShaderNodeBrightContrast', 'BRIGHTCONTRAST', 'Bright Contrast'),
    )
shaders_vector_submenu_items = (
    ('ShaderNodeMapping', 'MAPPING', 'Mapping'),
    ('ShaderNodeBump', 'BUMP', 'Bump'),
    ('ShaderNodeNormalMap', 'NORMAL_MAP', 'Normal Map'),
    ('ShaderNodeNormal', 'NORMAL', 'Normal'),
    ('ShaderNodeVectorCurve', 'CURVE_VEC', 'Vector Curves'),
    ('ShaderNodeVectorTransform', 'VECT_TRANSFORM', 'Vector Transform'),n
    )
shaders_converter_submenu_items = (
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
shaders_layout_submenu_items = (
    ('NodeReroute', 'REROUTE', 'Reroute'),
    )

# compositing nodes
compo_input_submenu_items = (
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
compo_output_submenu_items = (
        ('CompositorNodeComposite', 'COMPOSITE', 'Composite'),
    ('CompositorNodeViewer', 'VIEWER', 'Viewer'),
    ('CompositorNodeSplitViewer', 'SPLITVIEWER', 'Split Viewer'),
    ('CompositorNodeOutputFile', 'OUTPUT_FILE', 'File Output'),
    ('CompositorNodeLevels', 'LEVELS', 'Levels'),
    )
compo_color_submenu_items = (
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
compo_converter_submenu_items = (
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
compo_filter_submenu_items = (
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
compo_vector_submenu_items = (
    ('CompositorNodeNormal', 'NORMAL', 'Normal'),
    ('CompositorNodeMapValue', 'MAP_VALUE', 'Map Value'),
    ('CompositorNodeMapRange', 'MAP_RANGE', 'Map Range'),
    ('CompositorNodeNormalize', 'NORMALIZE', 'Normalize'),
    ('CompositorNodeCurveVec', 'CURVE_VEC', 'Vector Curves'),
    )
compo_matte_submenu_items = (
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
compo_distort_submenu_items = (
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
compo_layout_submenu_items = (
    ('NodeReroute', 'REROUTE', 'Reroute'),
    ('CompositorNodeSwitch', 'SWITCH', 'Switch'),
    )
