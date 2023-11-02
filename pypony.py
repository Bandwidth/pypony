import sys
import traceback

import click

from src.validate import validate


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-st", "--step_file", required=True, type=click.STRING, envvar="INPUT_STEP_FILE"
)
@click.option(
    "-sp", "--spec_file", required=True, type=click.STRING, envvar="INPUT_SPEC_FILE"
)
@click.option("-ff", "--fail-fast", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
def main(step_file, spec_file, fail_fast, verbose):
    try:
        validate(step_file, spec_file, fail_fast, verbose)
    except BaseException as e:
        if verbose:
            print(traceback.format_exc())
        else:
            print(str(e))

        sys.exit(1)


main()
