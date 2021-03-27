import numpy as np
from ..types.opengl_vectorized_mobject import OpenGLVMobject
from .svg_path import SVGPathMobject


class OpenGLSVGPathMobject(OpenGLVMobject, SVGPathMobject):
    def __init__(self, path_string, **kwargs):
        self.path_string = path_string
        OpenGLVMobject.__init__(self, **kwargs)
        self.current_path_start = np.zeros((1, self.dim))

    def init_points(self):
        self.generate_points()

    def start_new_path(self, point):
        SVGPathMobject.start_new_path(self, point)
