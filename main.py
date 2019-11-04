#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Nathan Smeal"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger
from scraping import scraper


def main(args: argparse.Namespace) -> None:
    """ Main entry point of the app """
    logger.info(args)
    success = scraper.capture_vid_captions(args.url, args.out)
    if success:
        logger.info("Video succesfully processed")
    else:
        logger.info("There was a problem with processing.  Check the logs.")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("url", help="Youtube url")
    parser.add_argument("-o", "--out", help="Output dir", default="./output/")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
