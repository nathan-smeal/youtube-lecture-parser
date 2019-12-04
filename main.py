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
from q_generator.model import Model
from q_generator.ocr_model import OCRModel
from typing import List
from q_generator.q_generator import QuestionGenerator


def main(args: argparse.Namespace) -> None:
    """ Main entry point of the app """
    logger.info(args)
    correlations = scraper.capture_vid_captions(args.url, args.out)
    logger.info(correlations[0])

    ocr_model = OCRModel()
    models: List[Model] = [ocr_model]
    qg = QuestionGenerator(models)
    questions = qg.generate_questions(correlations)
    for q in questions:
        q.base_to_file("./output/questions/current")

    if correlations is not None:
        logger.info("Video succesfully processed")
    else:
        logger.info("There was a problem with processing.  Check the logs.")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("url", help="Youtube url")
    parser.add_argument("-o", "--out", help="Output dir", default="./output/")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
