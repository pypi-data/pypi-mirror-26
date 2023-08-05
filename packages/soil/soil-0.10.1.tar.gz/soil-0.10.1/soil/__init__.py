import importlib
import sys
import os
import pdb
import logging

__version__ = "0.10.1"

try:
    basestring
except NameError:
    basestring = str

logging.basicConfig()

from . import agents
from . import simulation
from . import environment
from . import utils
from . import analysis


def main():
    import argparse
    from . import simulation

    parser = argparse.ArgumentParser(description='Run a SOIL simulation')
    parser.add_argument('file', type=str,
                        nargs="?",
                        default='simulation.yml',
                        help='python module containing the simulation configuration.')
    parser.add_argument('--module', '-m', type=str,
                        help='file containing the code of any custom agents.')
    parser.add_argument('--dry-run', '--dry', action='store_true',
                        help='Do not store the results of the simulation.')
    parser.add_argument('--pdb', action='store_true',
                        help='Use a pdb console in case of exception.')
    parser.add_argument('--output', '-o', type=str,
                        help='folder to write results to. It defaults to the current directory.')

    args = parser.parse_args()

    if args.module:
        sys.path.append(os.getcwd())
        importlib.import_module(args.module)

    logging.info('Loading config file: {}'.format(args.file, args.output))

    try:
        simulation.run_from_config(args.file, dump=(not args.dry_run), results_dir=args.output)
    except Exception as ex:
        if args.pdb:
            pdb.post_mortem()
        else:
            raise


if __name__ == '__main__':
    main()
