"""
cfg_file_utils.py
------------

Inputs the configuration files while checking it is valid. Can be executed by `manim-cfg` command.

"""
import os
import configparser

from .config_utils import _run_config, _paths_config_file, curr_config_dict

from rich.console import Console
from rich.progress import track
from rich.style import Style
from rich.errors import StyleSyntaxError

__all__ = ["write","show","export"]

INVALID_STYLE_MSG = "[red bold]Your Style is not valid. Try again.[/red bold]"
INTRO_INSTRUCTIONS = """[red]The default colour is used by the input statement.
If left empty, the default colour will be used.[/red]
[magenta] For a full list of styles, visit[/magenta] https://rich.readthedocs.io/en/latest/style.html"""
TITLE_TEXT = "[yellow bold]Manim Configuration File Writer[/yellow bold]"

console = Console()

def is_valid_style(style):
    """Checks whether the entered color is a valid color according to rich
    Parameters
    ----------
    style : :class:`str`
        The style to check whether it is valid.
    Returns
    -------
    Boolean
        Returns whether it is valid style or not according to rich.
    """
    try:
        Style.parse(style)
        return True
    except StyleSyntaxError:
        return False


def replace_keys(default):
    """Replaces _ to . and viceversa in a dictionary for rich
    Parameters
    ----------
    default : :class:`dict`
        The dictionary to check and replace
    Returns
    -------
    :class:`dict`
        The dictionary which is modified by replcaing _ with . and viceversa
    """
    for key in default:
        if "_" in key:
            temp = default[key]
            del default[key]
            key = key.replace("_", ".")
            default[key] = temp
        else:
            temp = default[key]
            del default[key]
            key = key.replace(".", "_")
            default[key] = temp
    return default


def write(level=None):
    config = _run_config()[1]
    default = config["logger"]
    console.print(TITLE_TEXT, justify="center")
    console.print(INTRO_INSTRUCTIONS)
    default = replace_keys(default)
    for key in default:
        console.print("Enter the Style for %s" % key + ":", style=key, end="")
        temp = input()
        if temp:
            while not is_valid_style(temp):
                console.print(INVALID_STYLE_MSG)
                console.print("Enter the Style for %s" % key + ":", style=key, end="")
                temp = input()
            else:
                default[key] = temp
    default = replace_keys(default)
    config["logger"] = default

    if level is None:
        console.print(
            "Do you want to save this as the default for this User?(y/n)[[n]]",
            style="dim purple",
            end="",
        )
        save_to_userpath = input()
    else:
        save_to_userpath = ""

    config_paths = _paths_config_file() + [os.path.abspath("manim.cfg")]
    if save_to_userpath.lower() == "y" or level=="user":
        if not os.path.exists(os.path.abspath(os.path.join(config_paths[1], ".."))):
            os.makedirs(os.path.abspath(os.path.join(config_paths[1], "..")))
        with open(config_paths[1], "w") as fp:
            config.write(fp)
        console.print(
            f"""A configuration file at [yellow]{config_paths[1]}[/yellow] has been created with your required changes.
This will be used when running the manim command. If you want to override this config,
you will have to create a manim.cfg in the local directory, where you want those changes to be overridden."""
        )
    else:
        with open(config_paths[2], "w") as fp:
            config.write(fp)
        console.print(
            f"""A configuration file at [yellow]{config_paths[2]}[/yellow] has been created.
To save your theme please save that file and place it in your current working directory, from where you run the manim command."""
        )

def show():
    current_config = curr_config_dict()
    for category in current_config:
        console.print(f"{category}",style="bold green underline")
        for entry in current_config[category]:
            if category=="logger":
                console.print(f"{entry} :",end="")
                console.print(
                    f" {current_config[category][entry]}",
                    style=current_config[category][entry]
                    )
            else:
                console.print(f"{entry} : {current_config[category][entry]}")
        console.print("\n")

def export(path):
    config = _run_config()[1]
    with open(os.path.join(path,"manim.cfg"),"w") as outpath:
        config.write(outpath)
        from_path = os.path.join(os.getcwd(),'manim.cfg')
        to_path = os.path.join(path,'manim.cfg')
    console.print(f"Exported final Config at {from_path} to {to_path}.")
