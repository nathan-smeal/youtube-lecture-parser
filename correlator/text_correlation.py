"""This file is a data class for text only correlation
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class TextCorrelation:
    """Class for correlation data for captions and frames
    Note:  Timestamps here are 5s before start time

    Arguments:
        caption {str} -- caption text
        yt_link {str} -- youtube url for reference
        timestamps {float} -- timestamp in milliseconds
    """

    caption: str
    yt_link: str  # required now
    timestamps: float

    def yt_ts_link(self) -> str:
        seconds = int(self.timestamps // 1000)
        return f"{self.yt_link}&t={str(seconds)}s"
