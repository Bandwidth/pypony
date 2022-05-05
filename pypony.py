import sys
import traceback
import click

from src.validate import verify_api


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--spec_file", required=True, type=click.STRING, envvar="INPUT_SPEC_FILE"
)
@click.option(
    "--step_file", required=True, type=click.STRING, envvar="INPUT_STEP_FILE"
)
@click.option(
    "-ff", "--fail-fast", is_flag=True
)
@click.option(
    "-v", "--verbose", is_flag=True
)
def main(spec_file, step_file, fail_fast, verbose):
    try:
        verify_api(spec_file, step_file, fail_fast, verbose)
    except BaseException as e:
        if verbose:
            print(traceback.format_exc())
        else:
            print(str(e))

        sys.exit(1)


main()
