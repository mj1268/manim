from manim.typing import Vector3D
import numpy as np
from manim.constants import DL, UR
from manim.mobject.opengl.opengl_mobject import OpenGLMobject as Mobject
from typing import Sequence

from .three_d_scene import ThreeDScene
from .states.display_keypress import DisplayKeypress
from .states.display_mouse_coords import DisplayMouseCoords

__all__ = ["InteractiveScene"]

class InteractiveScene(ThreeDScene):
    """
    This is a 3D scene with default user interaction tools.

    Features:
    - Camera control
    - Mouse coordinates
    - Selection of Mobjects
    - Hiding and unhiding of Mobjects (opacity)
    - Keyboard press event display
    """

    display_keypresses: bool = True
    last_keypress: DisplayKeypress | None = None

    display_mouse_coords: bool = True
    mouse_coords: DisplayMouseCoords | None = None

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
    
    def on_key_press(self, symbol, modifiers):
        self.handle_key_press_display(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.handle_key_release_display(symbol, modifiers)

    def on_mouse_motion(self, point: Vector3D, dpoint: Vector3D):
        self.handle_mouse_coords_display(point)

    def handle_key_press_display(self, symbol, modifiers):
        if not self.display_keypresses:
            return
        if self.last_keypress is not None:
            self.remove(self.last_keypress)
        disp_kp = DisplayKeypress(symbol, modifiers).scale(0.4).to_edge(DL)
        self.add(disp_kp)
        self.last_keypress = disp_kp

    def handle_key_release_display(self, symbol, modifiers):
        if self.last_keypress:
            self.remove(self.last_keypress)
            self.last_keypress = None

    def handle_mouse_coords_display(self, point: Vector3D):
        if not self.display_mouse_coords:
            return
        
        if self.mouse_coords is None:
            self.mouse_coords = DisplayMouseCoords(point=point).scale(0.4).to_edge(UR)
            self.add(self.mouse_coords)
        else:
            self.mouse_coords.update_coords(point=point)
    
    def handle_reset(self):
        self.camera.reset()
        self.camera_target = np.array([0, 0, 0], dtype=np.float32)
    
    def handle_quit(self):
        self.quit_interaction

    def set_camera_orientation(
        self,
        phi: float | None = None,
        theta: float | None = None,
        gamma: float | None = None,
        zoom: float | None = None,
        focal_distance: float | None = None,
        frame_center: Mobject | Sequence[float] | None = None,
        **kwargs,
    ):
        """
        This method sets the orientation of the camera in the scene.

        Parameters
        ----------
        phi
            The polar angle i.e the angle between Z_AXIS and Camera through ORIGIN in radians.

        theta
            The azimuthal angle i.e the angle that spins the camera around the Z_AXIS.

        focal_distance
            The focal_distance of the Camera.

        gamma
            The rotation of the camera about the vector from the ORIGIN to the Camera.
        """
        super().set_camera_orientation(
            phi=phi,
            theta=theta,
            gamma=gamma,
            zoom=zoom,
            focal_distance=focal_distance,
            frame_center=frame_center,
            **kwargs,
        )