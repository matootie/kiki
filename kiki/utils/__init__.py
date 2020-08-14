"""Utils module

Top level of the kiki.utils module.
"""

import typing
import yaml
from click import echo


def load_config(
        file: str = "kiki.yml"
) -> typing.Dict[str, typing.Union[bool, int, str]]:
    """Loads configuration data from file

    This method is used to store convenient configuration data in a file
    and load from that instead of hard-coding values or providing them
    through the command line.

    Args:
      file: Optional path to the file, relative to the root of the project.

    Returns: |
      A dictionary with strings to bool, int or string values, representing
      the resulting configuration data.
    """

    # Try opening the configuration file and load the yaml data to Python
    # dictionary.
    try:
        with open(file) as config:
            data = yaml.load(config, Loader=yaml.Loader)
    except FileNotFoundError:
        # Set a default value for the configuration data; an empty dictionary.
        echo("WARNING: Unable to load config file")
        data = {}

    # Return the resulting data.
    return data
