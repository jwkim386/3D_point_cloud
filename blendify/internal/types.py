import numpy as np
import bpy
import bpy_types
from typing import Sequence, Union, Tuple, List

BlenderGroup = Union[bpy.types.Collection, bpy_types.Object]
Vector2df = Union[np.ndarray, Tuple[float, float]]
Vector2di = Union[np.ndarray, Tuple[int, int]]
Vector3d = Union[np.ndarray, Tuple[float,float,float]]
Vector4d = Union[np.ndarray, Tuple[float,float,float,float]]