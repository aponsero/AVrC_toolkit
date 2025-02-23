# src/avrc/commands/download.py
import click
from ..utils.zenodo import get_file_info, download_subset, ZENODO_SUBSETS

@click.command(name="download")
@click.argument("subset", type=click.Choice(["all", "hq", "phage"]), required=False)
@click.option("-o", "--output", default=".", help="Output directory")
@click.option("--list", is_flag=True, help="List available subsets")
def download_cmd(subset, output, list):
    """Download AVrC data subsets."""
    if list:
        file_info = get_file_info()
        if file_info:
            click.echo("\nAvailable subsets:")
            for name, info in ZENODO_SUBSETS.items():
                total_size = sum(
                    file_info[f["filename"]]["size"] 
                    for f in info["files"]
                    if f["filename"] in file_info
                )
                click.echo(f"{name}: {info['description']} ({total_size/1e9:.1f}GB)")
        return

    if not subset:
        raise click.UsageError(
            "Please specify a subset to download (all, hq, phage) or use --list to see available subsets"
        )

    try:
        if download_subset(subset, output):
            click.echo("\nDownload completed successfully!")
    except Exception as e:
        raise click.ClickException(str(e))