"""Entrypoint of the bot command-line interface.

This is the script you would use to interact with the bot server-side.

    Typical usage example:

    $ python runner.py --help
    $ python runner.py run --version v1.23.4-beta.5
"""

from kiki.utils.cli import cli


if __name__ == "__main__":
    # Call on the primary cli group.
    cli()
