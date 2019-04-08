import os
import click
from multiprocessing import Pool
from stat import ST_MODE, S_ISREG

from pyoracc.wrapper.segment import Segmentor

from pyoracc.atf.common.atffile import check_atf


def check_atf_message(segpathname, atftype, verbose):
    click.echo('\n Info: Parsing {0}.'.format(segpathname))
    try:
        check_atf(segpathname, atftype, verbose)
        click.echo('Info: Correctly parsed {0}.'.format(segpathname))
    except (SyntaxError, IndexError, AttributeError,
            UnicodeDecodeError) as e:
        click.echo("Info: Failed with message: {0} in {1}"
                   .format(e, segpathname))
        return -1


def check_and_process(pathname, atftype, segment, verbose=False):
    mode = os.stat(pathname)[ST_MODE]
    if S_ISREG(mode) and pathname.lower().endswith('.atf'):
        # It's a file, call the callback function
        if verbose:
            click.echo('Info: Parsing {0}.'.format(pathname))
        try:
            if segment:
                pool = Pool()
                segmentor = Segmentor(pathname, verbose)
                outfolder = segmentor.convert()
                if verbose:
                    click.echo('Info: Segmented into {0}.'.format(outfolder))
                process_ids = []
                with click.progressbar(os.listdir(outfolder),
                                       label='Info: Checking the files') as bar:
                    for index, f in enumerate(bar):
                        segpathname = os.path.join(outfolder, f)
                        process_ids.append(pool.apply(
                            check_atf_message, (segpathname, atftype, verbose)))
            else:
                check_atf_message(pathname, atftype, verbose)
            click.echo('Info: Finished parsing {0}.'.format(pathname))
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
@click.option('--segment_disable', '-s', default=True, required=False, is_flag=True,
              help='Disables the segmentation of the atf file.')
@click.option('--verbose', '-v', default=False, required=False, is_flag=True,
              help='Enables verbose mode.')
@click.version_option()
def main(input_path, atf_type, segment, verbose):
    """My Tool does one work, and one work well."""
    pool = Pool()
    if os.path.isdir(input_path):
        process_ids = []
        with click.progressbar(os.listdir(input_path),
                               label='Info: Checking the files') as bar:
            for index, f in enumerate(bar):
                pathname = os.path.join(input_path, f)
                process_ids.append(pool.apply_async(
                    check_and_process, (pathname, atf_type, segment, verbose)))

        result = map(lambda x: x.get(), process_ids)
        successes = sum(filter(lambda x: (x == 1), result))
        failures = -sum(filter(lambda x: (x == -1), result))
        click.echo("Failed with {0} out of {1} ({2}%)"
                   .format(failures, failures + successes,
                           failures * 100.0 / (failures + successes)))
    else:
        check_and_process(input_path, atf_type, segment, verbose)
