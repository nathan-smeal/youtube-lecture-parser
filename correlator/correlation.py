"""This file is a data class for correlation
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from .text_correlation import TextCorrelation


@dataclass
class Correlation(TextCorrelation):
    "Class for correlation data for captions and frames"
    ocr_boxes: pd.DataFrame
    frame: np.array

    def simple_score(self) -> float:
        # a separate NLP, another similarity may use cosine of vectorized sentences.
        # this needs to be really light, as other methods will have more robust comparisons (eq detect)
        return jaccard_similarity(query=self.ocr_block_text(), document=self.caption)

    def ocr_block_text(self, conf_thresh=70) -> str:
        # columns = [
        #     "level",
        #     "page_num",
        #     "block_num",
        #     "par_num",
        #     "line_num",
        #     "word_num",
        #     "left",
        #     "top",
        #     "width",
        #     "height",
        #     "conf",
        #     "text",
        # ]
        result = ""
        thresholded = self.ocr_boxes[self.ocr_boxes.conf > conf_thresh]
        thresholded = thresholded.astype(str)
        thresholded = thresholded.dropna()
        result = thresholded["text"].str.cat(sep=" ")
        # could use confidence from
        return result


def jaccard_similarity(query, document) -> float:
    # https://medium.com/@adriensieg/text-similarities-da019229c894
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection) / len(union)
