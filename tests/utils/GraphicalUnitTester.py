import numpy as np
import os
import sys
import inspect
import logging
import pytest
import warnings
from platform import system

from manim import config


class GraphicalUnitTester:
    """Class used to test the animations.

    Parameters
    ----------
    scene_object : :class:`~.Scene`
        The scene to be tested
    config_scene : :class:`dict`
        The configuration of the scene
    module_tested : :class:`str`
        The name of the module tested. i.e if we are testing functions of creation.py, the module will be "creation"

    Attributes
    -----------
    path_tests_medias_cache : : class:`str`
        Path to 'media' folder generated by manim. This folder contains cached data used by some tests.
    path_control_data : :class:`str`
        Path to the data used for the tests (i.e the pre-rendered frames).
    scene : :class:`Scene`
        The scene tested
    """

    def __init__(
        self,
        scene_object,
        module_tested,
        tmpdir,
    ):
        # Disable the the logs, (--quiet is broken) TODO
        logging.disable(logging.CRITICAL)
        tests_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path_tests_medias_cache = os.path.join(
            tmpdir,
            "test_graphical_units",
            "tests_cache",
            module_tested,
            scene_object.__name__,
        )
        self.path_control_data = os.path.join(
            tests_directory, "control_data", "graphical_units_data", module_tested
        )

        # IMPORTANT NOTE : The graphical units tests don't use for now any
        # custom manim.cfg, since it is impossible to manually select a
        # manim.cfg from a python file. (see issue #293)
        config["text_dir"] = os.path.join(self.path_tests_medias_cache, "Text")
        config["tex_dir"] = os.path.join(self.path_tests_medias_cache, "Tex")

        config["skip_animations"] = True
        config["save_last_frame"] = True
        config["write_to_movie"] = False
        config["disable_caching"] = True
        config["quality"] = "low_quality"

        for dir_temp in [
            self.path_tests_medias_cache,
            config["text_dir"],
            config["tex_dir"],
        ]:
            os.makedirs(dir_temp)

        # By invoking this, the scene is rendered.
        self.scene = scene_object()
        self.scene.render()

    def _load_data(self):
        """Load the np.array of the last frame of a pre-rendered scene. If not found, throw FileNotFoundError.

        Returns
        -------
        :class:`numpy.array`
            The pre-rendered frame.
        """
        frame_data_path = os.path.join(
            os.path.join(self.path_control_data, "{}.npy".format(str(self.scene)))
        )
        return np.load(frame_data_path)

    def _show_diff_helper(self, frame_data, expected_frame_data):
        """Will visually display with matplotlib differences between frame generared and the one expected."""
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec

        gs = gridspec.GridSpec(2, 2)
        fig = plt.figure()
        fig.suptitle(f"Test for {str(self.scene).replace('Test', '')}", fontsize=16)

        ax = fig.add_subplot(gs[0, 0])
        ax.imshow(frame_data)
        ax.set_title("Generated :")

        ax = fig.add_subplot(gs[0, 1])
        ax.imshow(expected_frame_data)
        ax.set_title("Expected :")

        ax = fig.add_subplot(gs[1, :])
        diff_im = expected_frame_data.copy()
        diff_im = np.where(
            frame_data != np.array([0, 0, 0, 255]),
            np.array([255, 0, 0, 255], dtype="uint8"),
            np.array([0, 0, 0, 255], dtype="uint8"),
        )  # Set the points of the frame generated to red.
        np.putmask(
            diff_im,
            expected_frame_data != np.array([0, 0, 0, 255], dtype="uint8"),
            np.array([0, 255, 0, 255], dtype="uint8"),
        )  # Set the points of the frame generated to green.
        ax.imshow(diff_im, interpolation="nearest")
        ax.set_title("Differences summary : (red = got, green = expected)")

        plt.show()

    def test(self, show_diff=False):
        """Compare pre-rendered frame to the frame rendered during the test."""
        frame_data = self.scene.get_frame()
        expected_frame_data = self._load_data()

        assert frame_data.shape == expected_frame_data.shape, (
            "The frames have different shape:"
            + f"\nexpected_frame_data.shape = {expected_frame_data.shape}"
            + f"\nframe_data.shape = {frame_data.shape}"
        )

        test_result = np.array_equal(frame_data, expected_frame_data)
        if not test_result:
            incorrect_indices = np.argwhere(frame_data != expected_frame_data)
            first_incorrect_index = incorrect_indices[0][:2]
            first_incorrect_point = frame_data[tuple(first_incorrect_index)]
            expected_point = expected_frame_data[tuple(first_incorrect_index)]
            if show_diff:
                self._show_diff_helper(frame_data, expected_frame_data)
            assert test_result, (
                f"The frames don't match. {str(self.scene).replace('Test', '')} has been modified."
                + "\nPlease ignore if it was intended."
                + f"\nFirst unmatched index is at {first_incorrect_index}: {first_incorrect_point} != {expected_point}"
            )
