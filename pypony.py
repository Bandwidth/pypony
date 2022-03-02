import sys
import traceback

import click
from actions_toolkit import core

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
    "-ff", "--fail-fast", default=False, type=click.BOOL, envvar="INPUT_FAIL_FAST"
)
@click.option(
    "-v", "--verbose", default=False, type=click.BOOL, envvar="INPUT_VERBOSE"
)
def main(spec_file, step_file, fail_fast, verbose):
    try:
        verify_api(spec_file, step_file, fail_fast, verbose)
    except BaseException as e:
        if verbose:
            core.error(traceback.format_exc(), title=e.__class__.__name__)
        else:
            core.error(str(e), title=e.__class__.__name__)

        sys.exit(1)


main()
