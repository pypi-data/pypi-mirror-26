import importlib
import sys
import os
import argparse
import logging
from . import simulation

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(description='Run a SOIL simulation')
    parser.add_argument('file', type=str,
                        nargs="?",
                        default='simulation.yml',
                        help='python module containing the simulation configuration.')
    parser.add_argument('--module', '-m', type=str,
                        help='file containing the code of any custom agents.')
    parser.add_argument('--dry-run', '--dry', action='store_true',
                        help='Do not store the results of the simulation.')
    parser.add_argument('--output', '-o', type=str,
                        help='folder to write results to. It defaults to the current directory.')

    args = parser.parse_args()

    if args.module:
        sys.path.append(os.getcwd())
        importlib.import_module(args.module)

    print('Loading config file: {}'.format(args.file, args.output))
    simulation.run_from_config(args.file, dump=not args.dry_run, results_dir=args.output)


if __name__ == '__main__':
    main()
