"""Entrypoint of the bot command-line interface.

This is the script you would use to interact with the bot server-side.

  Typical usage example: |

    $ python kiki --help
    $ python kiki run
"""

from utils.cli import cli

if __name__ == "__main__":
    # Call on the primary cli group.
    cli()
