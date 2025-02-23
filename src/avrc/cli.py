# src/avrc/cli.py
import click
from .commands.download import download_cmd
from .commands.filter import filter_cmd

@click.group()
@click.version_option()
def main():
    """AVrC toolkit for downloading and filtering viral sequences."""
    pass

main.add_command(download_cmd)
main.add_command(filter_cmd)

if __name__ == "__main__":
    main()
