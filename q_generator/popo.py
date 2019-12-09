"""Plain old python objects
This file contains some simple data objects for use in question generating
"""
from dataclasses import dataclass
import numpy as np
from os import path
import cv2
import json

from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


@dataclass
class BaseQuestion:
    "Base Class for question data; no image"
    question: str
    answer: str
    yt_link: str
    confidence: float

    def base_to_file(self, out_dir) -> None:
        img_out = path.join(
            out_dir,
            self.yt_link.replace("https://www.youtube.com/watch?v=", "") + ".json",
        )
        with open(img_out, "w") as out:
            json.dump(
                MyEncoder().encode(self), out, skipkeys=True, sort_keys=True, indent=2
            )


@dataclass
class Question(BaseQuestion):
    "Class for question data"
    frame: np.array = None


@dataclass
class Flashcard(BaseQuestion):
    "Flashcard format for question(question == hint)"

    frame: np.array = None

    def export_to_json_file(self, out_dir):
        img_out = path.join(out_dir, self.yt_link + ".png")
        cv2.imwrite(img_out, self.frame)

    def export_to_images(self, outdir):
        # write hint
        pass
