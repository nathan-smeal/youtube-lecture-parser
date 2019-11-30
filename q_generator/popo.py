"""Plain old python objects
This file contains some simple data objects for use in question generating
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class Question:
    "Class for question data"
    question: str
    answer: str
    yt_link: str = ""
    frame: np.array = None
