"""Console script for django_codemod."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for django_codemod."""
    click.echo("Hello")
    click.echo("See more https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
