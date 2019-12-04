"""This is a OCR with rule based model for finding question candidates.
"""
from .model import Model
from typing import List
from .popo import Question
from correlator.correlation import Correlation
from .popo import BaseQuestion


class OCRModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.threshold = 0.80

    def generate_questions(self) -> List[Question]:
        super().generate_questions
        return []

    def process_correlation(self, correlation: Correlation) -> BaseQuestion:
        if correlation.simple_score() > self.threshold:
            # TODO: more advanced model would use NER
            return BaseQuestion(
                question=correlation.ocr_block_text(),
                answer=correlation.caption,
                yt_link=correlation.yt_ts_link(),
                confidence=correlation.simple_score(),
            )
        else:
            # not good enough correlation
            return None
