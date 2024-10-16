from manim.constants import DOWN, RIGHT
import numpy as np
from manim.mobject.text.numbers import DecimalNumber
from manim.typing import Vector3D
from manim.opengl import OpenGLVGroup
import time

class DisplayMouseCoords(OpenGLVGroup):
    """Display keypresses on the screen."""
    x: DecimalNumber
    y: DecimalNumber
    z: DecimalNumber
    last_update_time: float = 0.0

    def __init__(
        self,
        point: Vector3D = np.array([0.0, 0.0, 0.0]),
        *args,
        **kwargs
    ):
        super().__init__()

        default_style = dict(
            fill_opacity=1.0,
            color="#FFFFFF",
            stroke_width=None,
            num_decimal_places=2,
            include_sign=True,
            edge_to_fix=RIGHT,
        )
        self.x = DecimalNumber(point[0], *args, **default_style, **kwargs)
        self.y = DecimalNumber(point[1], *args, **default_style, **kwargs)
        self.z = DecimalNumber(point[2], *args, **default_style, **kwargs)

        self.add(self.x, self.y, self.z)
        self.arrange(DOWN)


    def update_coords(self, point: Vector3D):
        # Standoff time to prevent buffering slowdown
        if time.time() - self.last_update_time < 0.05:
            return None
        self.last_update_time = time.time()

        self.x.set_value(point[0])
        self.y.set_value(point[1])
        self.z.set_value(point[2])