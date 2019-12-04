"""Abstract Base class for question generating model.
"""

from abc import ABCMeta, abstractclassmethod, abstractmethod, ABC
from .popo import Question, BaseQuestion
from typing import List
from correlator.correlation import Correlation


class Model(ABC):
    def __init__(self) -> None:
        self.info_loaded = False

    def start(self):
        pass

    def stop(self):
        pass

    def load_captions(self, captions):
        pass

    @abstractmethod
    def process_correlation(self, correlation: Correlation) -> BaseQuestion:
        return None

    @abstractmethod
    def generate_questions(self) -> List[Question]:
        assert self.info_loaded
        return []
