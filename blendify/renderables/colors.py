import bpy
import bpy_types
import numpy as np
from abc import ABC, abstractmethod
from typing import Union, Tuple, List, Sequence


class Colors(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_blender_colornode(self, object_material: bpy.types.Material) -> bpy_types.ShaderNode:
        pass


class VertexColors(Colors):
    def __init__(self, vertex_colors: np.ndarray):
        super().__init__()
        self.vertex_colors = vertex_colors

    def create_blender_colornode(self, object_material) -> bpy_types.ShaderNode:
        vertex_color = object_material.node_tree.nodes.new('ShaderNodeVertexColor')
        return vertex_color


class UniformColors(Colors):
    def __init__(self, uniform_color: Union[np.ndarray, Sequence[float]]):
        super().__init__()
        self.color = uniform_color

    def create_blender_colornode(self, object_material: bpy.types.Material) -> bpy_types.ShaderNode:
        color_node = object_material.node_tree.nodes.new('ShaderNodeRGB')
        color_node.outputs[0].default_value = self.color.tolist() + [1.]
        return color_node

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, uniform_color):
        uniform_color = np.array(uniform_color)
        assert len(uniform_color) == 3, "Color should be in RGB format"
        assert uniform_color.max() <= 1. and uniform_color.min() >= 0., "Color values should be in [0,1] range"
        self._color = uniform_color


class UVColors(Colors):
    @abstractmethod
    def __init__(self, uv_map: np.ndarray):
        super().__init__()
        self.uv_map = uv_map


class TextureColors(UVColors):
    def __init__(self, texture: np.ndarray, uv_map: np.ndarray):
        super().__init__(uv_map)
        self.texture = texture

    def create_blender_colornode(self, object_material: bpy.types.Material) -> bpy_types.ShaderNode:
        object_texture = object_material.node_tree.nodes.new('ShaderNodeTexImage')
        raise NotImplementedError("Assigning textures from memory is not implemented yet")
        return object_texture


class FileTextureColors(UVColors):
    def __init__(self, texture_path: str, uv_map: np.ndarray):
        super().__init__(uv_map)
        self.texture_path = texture_path

    def create_blender_colornode(self, object_material: bpy.types.Material) -> bpy_types.ShaderNode:
        object_texture = object_material.node_tree.nodes.new('ShaderNodeTexImage')
        object_texture.image = self.texture_path
        return object_texture