# THE CODE BELOW IS GENERATED BY PYBASHRC
import inspect
import os
import sys
from pathlib import Path

from rich import print

import pybashrc.pybashrc_link as pybashrc_link

_INSTALL_DIR = Path(os.environ["PYBASHRC_INSTALL_DIR"])


# If pybashrc contains an __all__, simply import all functions from there
if hasattr(pybashrc_link, "__all__"):
    _FUNCTIONS = {}
    for name in getattr(pybashrc_link, "__all__"):
        object = getattr(pybashrc_link, name)
        if inspect.isfunction(object):
            _FUNCTIONS[name] = object

# If not, import all functions that are in its scope that do not start with _ and
# actually originate from the file itself (i.e. they must not be imported)
else:
    file_path = str(_INSTALL_DIR / "pybashrc_link.py")
    _FUNCTIONS = {}
    for name in dir(pybashrc_link):
        object = getattr(pybashrc_link, name)
        if (
            not name.startswith("_")
            and inspect.isfunction(object)
            and inspect.getfile(object) == file_path
        ):
            _FUNCTIONS[name] = object


def _get_function_info(func):
    string = f"{func.__name__}{inspect.signature(func)}"
    if func.__doc__:
        string += f"\n    {func.__doc__}"
    return string


def _update_aliases():
    aliases = (_INSTALL_DIR / "templates" / ".pybashrc_aliases").read_text()
    for name in _FUNCTIONS.keys():
        aliases += f"alias {name}='pybash {name}'\n"
    (_INSTALL_DIR / ".pybashrc_aliases").write_text(aliases)


if __name__ == "__main__":
    print(_FUNCTIONS)
    if len(sys.argv) < 2:
        print("Available functions:")
        for function in _FUNCTIONS.values():
            print(f"- {_get_function_info(function)}")
        exit(0)

    name = sys.argv[1]

    # System command not intended to be accessed by the user
    if name == "_update_aliases":
        _update_aliases()
        exit(0)

    # Parse arguments and keyword arguments
    args = []
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=")
            kwargs[key] = value
        else:
            args.append(arg)

    if name in _FUNCTIONS.keys():
        _FUNCTIONS[name](*args, **kwargs)
    else:
        raise ValueError(f"pybashrc received unknown function name {name}!")