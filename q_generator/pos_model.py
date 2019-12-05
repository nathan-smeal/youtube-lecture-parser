"""Parts of speech model - uses parts of speech and rules to make substitution based questions.
"""

import nltk
from .model import Model
from .simple_nlp import remove_markup
from scraping import clean_srt_nlp
from logzero import logging


class PosModel(Model):
    def tokenize(self, text: str):
        result = clean_srt_nlp.remove_time_stamps(text)
        result = remove_markup(result)
        result = nltk.word_tokenize(result)
        return result

    def pos_tag(self, tokens):
        return nltk.pos_tag(tokens)

    def subject_phrase(self):
        pass

    def start(self):
        # no tf model or anything that requires starting
        pass

    def stop(self):
        # no tf model or anything that requires stopping
        pass

    def load_captions(self, captions):
        return super().load_captions(captions)

    def process_correlation(self, correlation):
        return super().process_correlation(correlation)

    def generate_questions(self):
        if self.captions is None:
            logging.INFO("Attempted to generate questions without loading captions")
            return []
        # TODO
        return super().generate_questions()
