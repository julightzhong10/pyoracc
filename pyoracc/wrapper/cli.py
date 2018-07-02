import os
import click
from multiprocessing import Pool
from stat import ST_MODE, S_ISREG

from pyoracc.atf.common.atffile import check_atf


def check_and_process(pathname, atftype, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.atf'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Info: Parsing {0}.'.format(pathname))
        try:
            check_atf(pathname, atftype, verbose)
            click.echo('Info: Correctly parsed {0}.'.format(pathname))
            return 1
        except (SyntaxError, IndexError, AttributeError,
                UnicodeDecodeError) as e:
            click.echo("Info: Failed with message: {0} in {1}"
                       .format(e, pathname))
            return -1


@click.command()
@click.option('--input_path', '-i',
              type=click.Path(exists=True, writable=True), prompt=True,
              required=True,
              help='Input the file/folder name.')
@click.option('--atf_type', '-f', type=click.Choice(['cdli', 'oracc']),
              prompt=True, required=True,
              help='Input the atf file type.')
# @click.option('--segment', '-s', default=False, required=False, is_flag=True,
#              help='Enables the segmentation of the atf file with error.')
@click.option('-v', '--verbose', default=False, required=False, is_flag=True,
              help='Enables verbose mode.')
@click.version_option()
def main(input_path, atf_type, verbose):
    """My Tool does one work, and one work well."""
    pool = Pool()
    if os.path.isdir(input_path):
        process_ids = []
        with click.progressbar(os.listdir(input_path),
                               label='Info: Checking the files') as bar:
            for index, f in enumerate(bar):
                pathname = os.path.join(input_path, f)
                process_ids.append(pool.apply_async(
                    check_and_process, (pathname, atf_type, verbose)))

        result = map(lambda x: x.get(), process_ids)
        successes = sum(filter(lambda x: (x == 1), result))
        failures = -sum(filter(lambda x: (x == -1), result))
        click.echo("Failed with {0} out of {1} ({2}%)"
                   .format(failures, failures + successes,
                           failures * 100.0 / (failures + successes)))
    else:
        check_and_process(input_path, atf_type, verbose)
