"""Interface for writing, compiling, and converting ``.tex`` files.

.. SEEALSO::

    :mod:`.mobject.svg.tex_mobject`

"""

import os
import hashlib
from pathlib import Path

from .. import file_writer_config, config, logger


def tex_hash(expression):
    id_str = str(expression)
    hasher = hashlib.sha256()
    hasher.update(id_str.encode())
    # Truncating at 16 bytes for cleanliness
    return hasher.hexdigest()[:16]


def tex_to_svg_file(expression, environment=None, tex_template=None):
    """Takes a tex expression and returns the svg version of the compiled tex

    Parameters
    ----------
    expression : :class:`str`
        String containing the TeX expression to be rendered, e.g. ``\\sqrt{2}`` or ``foo``
    environment : :class:`str`
        The string containing the environment in which the expression should be typeset, e.g. ``align*``
        Optional. If not set, the expression will be rendered in text mode.
    tex_template : :class:`TexTemplate`
        Template class used to typesetting.
        Optional. If not set, the default template will be used.
    Returns
    -------
    Path to generated SVG file.
    """
    if tex_template is None:
        tex_template = config["tex_template"]
    tex_file = generate_tex_file(expression, environment, tex_template)
    dvi_file = tex_to_dvi(
        tex_file, tex_template.tex_compiler, tex_template.output_format
    )
    return dvi_to_svg(dvi_file, tex_template.output_format)


def generate_tex_file(expression, environment, tex_template):
    """Takes a tex expression (and an optional tex environment),
    and returns a fully formed tex file ready for compilation.

    Parameters
    ----------
    expression : :class:`str`
        String containing the TeX expression to be rendered, e.g. ``\\sqrt{2}`` or ``foo``
    environment : :class:`str`
        The string containing the environment in which the expression should be typeset, e.g. ``align*``
        Optional. If not set, the expression will be rendered in text mode.
    tex_template : :class:`TexTemplate`
        Template class used to typesetting.
        Optional. If not set, the default template will be used.
    Returns
    -------
    Generated TeX file ready for compilation
    """
    if environment is not None:
        output = tex_template.get_texcode_for_expression_in_env(expression, environment)
    else:
        output = tex_template.get_texcode_for_expression(expression)

    result = os.path.join(file_writer_config["tex_dir"], tex_hash(output)) + ".tex"
    if not os.path.exists(result):
        logger.info('Writing "%s" to %s' % ("".join(expression), result))
        with open(result, "w", encoding="utf-8") as outfile:
            outfile.write(output)
    return result


def tex_compilation_command(tex_compiler, output_format, tex_file, tex_dir):
    """Prepares the tex compilation command with all necessary cli flags

    Parameters
    ----------
    tex_compiler : :class:`str`
        String containing the compiler to be used, e.g. ``pdflatex`` or ``lualatex``
    output_format : :class:`str`
        String containing the output format generated by the compiler, e.g. ``.dvi`` or ``.pdf``
        Optional. If not set, the expression will be rendered in text mode.
    tex_file : :class:`str`
        File name of TeX file to be typeset.
    tex_dir : :class:`str`
        Path to the directory where compiler output will be stored.
    Returns
    -------
    Path to generated output file.
    """
    if tex_compiler in {"latex", "pdflatex", "luatex", "lualatex"}:
        commands = [
            tex_compiler,
            "-interaction=batchmode",
            f'-output-format="{output_format[1:]}"',
            "-halt-on-error",
            f'-output-directory="{tex_dir}"',
            f'"{tex_file}"',
            ">",
            os.devnull,
        ]
    elif tex_compiler == "xelatex":
        if output_format == ".xdv":
            outflag = "-no-pdf"
        elif output_format == ".pdf":
            outflag = ""
        else:
            raise ValueError("xelatex output is either pdf or xdv")
        commands = [
            "xelatex",
            outflag,
            "-interaction=batchmode",
            "-halt-on-error",
            '-output-directory="{}"'.format(tex_dir),
            '"{}"'.format(tex_file),
            ">",
            os.devnull,
        ]
    else:
        raise ValueError(f"Tex compiler {tex_compiler} unknown.")
    return " ".join(commands)


def tex_to_dvi(tex_file, tex_compiler, output_format):
    """Compiles a tex_file into a .dvi or a .xdv or a .pdf

    Parameters
    ----------
    tex_file : :class:`str`
        File name of TeX file to be typeset.
    tex_compiler : :class:`str`
        String containing the compiler to be used, e.g. ``pdflatex`` or ``lualatex``
    output_format : :class:`str`
        String containing the output format generated by the compiler, e.g. ``.dvi`` or ``.pdf``
        Optional. If not set, the expression will be rendered in text mode.
    Returns
    -------
    Path to generated output file.
    """
    result = tex_file.replace(".tex", output_format)
    result = Path(result).as_posix()
    tex_file = Path(tex_file).as_posix()
    tex_dir = Path(file_writer_config["tex_dir"]).as_posix()
    if not os.path.exists(result):
        command = tex_compilation_command(
            tex_compiler, output_format, tex_file, tex_dir
        )
        exit_code = os.system(command)
        if exit_code != 0:
            log_file = tex_file.replace(".tex", ".log")
            raise ValueError(
                f"{tex_compiler} error converting to"
                f" {output_format[1:]}. See log output above or"
                f" the log file: {log_file}"
            )
    return result


def dvi_to_svg(dvi_file, extension, regen_if_exists=False, page=1):
    """Converts a .dvi, .xdv, or .pdf file into an svg using dvisvgm.

    Parameters
    ----------
    dvi_file : :class:`str`
        File name of the input file to be converted.
    extension : :class:`str`
        String containing the file extension and thus indicating the file type, e.g. ``.dvi`` or ``.pdf``
    regen_if_exists : `bool`
        Setting if SVG has to be regenerated even if it already exists. Optional, defaulting to False.
    page : `int`
        Page to be converted if input file is multi-page. Optional, defaulting to 1.
    Returns
    -------
    Path to generated SVG file."""
    result = dvi_file.replace(extension, ".svg")
    result = Path(result).as_posix()
    dvi_file = Path(dvi_file).as_posix()
    if not os.path.exists(result):
        commands = [
            "dvisvgm",
            "--pdf" if extension == ".pdf" else "",
            "-p " + str(page),
            '"{}"'.format(dvi_file),
            "-n",
            "-v 0",
            "-o " + f'"{result}"',
            ">",
            os.devnull,
        ]
        os.system(" ".join(commands))
    return result
