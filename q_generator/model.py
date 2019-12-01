"""Abstract Base class for question generating model.
"""

from abc import ABCMeta, abstractclassmethod, abstractmethod, ABC
from .popo import Question
from typing import List


class Model(ABC):
    def __init__(self):
        self.info_loaded = False

    def load_captions(self, captions):
        pass

    def generate_questions(self) -> List[Question]:
        assert self.info_loaded
        return []
