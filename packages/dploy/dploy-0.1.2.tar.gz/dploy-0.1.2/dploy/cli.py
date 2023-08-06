"""
The command line interface
"""

import sys
import argparse
from dploy import linkcmd
from dploy import stowcmd
from dploy import version


def add_ignore_argument(parser):
    """
    adds the ignore argument to a subcmd parser
    """
    parser.add_argument(
        '--ignore',
        dest='ignore_patterns',
        action='append',
        default=None,
        help='glob pattern used to ignore directories')


def create_parser():
    """
    create the CLI argument parser
    """
    parser = argparse.ArgumentParser(prog='dploy')

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=version.__version__))
    parser.add_argument(
        '--silent',
        dest='is_silent',
        action='store_true',
        help='suppress all output')
    parser.add_argument(
        '--dry-run',
        dest='is_dry_run',
        action='store_true',
        help='show what would be done without doing it')

    sub_parsers = parser.add_subparsers(dest="subcmd")

    stow_parser = sub_parsers.add_parser('stow')
    stow_parser.add_argument(
        'source', nargs='+', help='source directory to stow')
    stow_parser.add_argument('dest', help='destination path to stow into')
    add_ignore_argument(stow_parser)

    unstow_parser = sub_parsers.add_parser('unstow')
    unstow_parser.add_argument(
        'source', nargs='+', help='source directory to unstow from')
    unstow_parser.add_argument('dest', help='destination path to unstow')
    add_ignore_argument(unstow_parser)

    link_parser = sub_parsers.add_parser('link')
    link_parser.add_argument('source', help='source file or directory to link')
    link_parser.add_argument('dest', help='destination path to link')
    add_ignore_argument(link_parser)
    return parser


def run(arguments=None):
    """
    interpret the parser arguments and execute the corresponding commands
    """

    subcmd_map = {
        'stow': stowcmd.Stow,
        'unstow': stowcmd.UnStow,
        'link': linkcmd.Link,
    }

    try:
        parser = create_parser()

        if arguments is None:
            args = parser.parse_args()
        else:
            args = parser.parse_args(arguments)

        try:
            subcmd = subcmd_map[args.subcmd]
            subcmd(
                args.source,
                args.dest,
                is_silent=args.is_silent,
                is_dry_run=args.is_dry_run,
                ignore_patterns=args.ignore_patterns)
        except (ValueError, PermissionError, FileNotFoundError,
                NotADirectoryError):
            sys.exit(1)
        except KeyError:
            parser.print_help()

    except (KeyboardInterrupt) as error:
        print(error, file=sys.stderr)
        sys.exit(130)
