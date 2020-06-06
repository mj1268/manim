import inspect
import itertools as it
import os
import platform
import subprocess as sp
import sys
import traceback
import importlib.util

from .config import file_writer_config
from .scene.scene import Scene
from .utils.sounds import play_error_sound
from .utils.sounds import play_finish_sound
from . import constants
from .logger import logger


def open_file_if_needed(file_writer):
    if file_writer_config["quiet"]:
        curr_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    open_file = any([
        file_writer_config["preview"],
        file_writer_config["show_file_in_finder"]
    ])
    if open_file:
        current_os = platform.system()
        file_paths = []

        if file_writer_config["save_last_frame"]:
            file_paths.append(file_writer.get_image_file_path())
        if file_writer_config["write_to_movie"]:
            file_paths.append(file_writer.get_movie_file_path())

        for file_path in file_paths:
            if current_os == "Windows":
                os.startfile(file_path)
            else:
                commands = []
                if current_os == "Linux":
                    commands.append("xdg-open")
                elif current_os.startswith("CYGWIN"):
                    commands.append("cygstart")
                else:  # Assume macOS
                    commands.append("open")

                if file_writer_config["show_file_in_finder"]:
                    commands.append("-R")

                commands.append(file_path)

                # commands.append("-g")
                FNULL = open(os.devnull, 'w')
                sp.call(commands, stdout=FNULL, stderr=sp.STDOUT)
                FNULL.close()

    if file_writer_config["quiet"]:
        sys.stdout.close()
        sys.stdout = curr_stdout


def is_child_scene(obj, module):
    if not inspect.isclass(obj):
        return False
    if not issubclass(obj, Scene):
        return False
    if obj == Scene:
        return False
    if not obj.__module__.startswith(module.__name__):
        return False
    return True


def prompt_user_for_choice(scene_classes):
    num_to_class = {}
    for count, scene_class in zip(it.count(1), scene_classes):
        name = scene_class.__name__
        print("%d: %s" % (count, name))
        num_to_class[count] = scene_class
    try:
        user_input = input(constants.CHOOSE_NUMBER_MESSAGE)
        return [
            num_to_class[int(num_str)]
            for num_str in user_input.split(",")
        ]
    except KeyError:
        logger.error(constants.INVALID_NUMBER_MESSAGE)
        sys.exit(2)
        user_input = input(constants.CHOOSE_NUMBER_MESSAGE)
        return [
            num_to_class[int(num_str)]
            for num_str in user_input.split(",")
        ]
    except EOFError:
        sys.exit(1)


def get_scenes_to_render(scene_classes):
    if not scene_classes:
        logger.error(constants.NO_SCENE_MESSAGE)
        return []
    if file_writer_config["write_all"]:
        return scene_classes
    result = []
    for scene_name in file_writer_config["scene_names"]:
        found = False
        for scene_class in scene_classes:
            if scene_class.__name__ == scene_name:
                result.append(scene_class)
                found = True
                break
        if not found and (scene_name != ""):
            logger.error(
                constants.SCENE_NOT_FOUND_MESSAGE.format(
                    scene_name
                )
            )
    if result:
        return result
    return [scene_classes[0]] if len(scene_classes) == 1 else prompt_user_for_choice(scene_classes)


def get_scene_classes_from_module(module):
    if hasattr(module, "SCENES_IN_ORDER"):
        return module.SCENES_IN_ORDER
    else:
        return [
            member[1]
            for member in inspect.getmembers(
                module,
                lambda x: is_child_scene(x, module)
            )
        ]


def get_module(file_name):
    if file_name == "-":
        module = types.ModuleType("input_scenes")
        code = sys.stdin.read()
        try:
            exec(code, module.__dict__)
            return module
        except Exception as e:
            logger.error(f"Failed to render scene: {str(e)}")
            sys.exit(2)
    else:
        if os.path.exists(file_name):
            module_name = file_name.replace(os.sep, ".").replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, file_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        else:
            raise FileNotFoundError(f'{file_name} not found')


def main():
    module = get_module(file_writer_config["input_file"])
    all_scene_classes = get_scene_classes_from_module(module)
    scene_classes_to_render = get_scenes_to_render(all_scene_classes)

    for SceneClass in scene_classes_to_render:
        try:
            # By invoking, this renders the full scene
            scene = SceneClass()
            open_file_if_needed(scene.file_writer)
            if file_writer_config["sound"]:
                play_finish_sound()
        except Exception:
            print("\n\n")
            traceback.print_exc()
            print("\n\n")
            if file_writer_config["sound"]:
                play_error_sound()


if __name__ == "__main__":
    main()
