"""Parts of speech model - uses parts of speech and rules to make substitution based questions.
"""

import nltk
from .model import Model
from .simple_nlp import remove_markup
from scraping import clean_srt_nlp
from logzero import logging
from correlator.text_correlation import TextCorrelation
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tree import Tree
from .popo import BaseQuestion


class PosModel(Model):
    # TODO:  Uncomment this out after ipython session (bug on reload)
    # def __init__(self):
    #     super().__init__()

    #     nltk.download("punkt")
    #     nltk.download('averaged_perceptron_tagger')

    def tokenize(self, text: str):
        # result = clean_srt_nlp.remove_time_stamps(text)
        result = remove_markup(text)
        result = nltk.word_tokenize(result)
        return result

    def pos_tag(self, tokens: list):
        return nltk.pos_tag(tokens)

    def subject_phrase(self, pos: list):
        chunkGram = r"""Chunk: {<WP.?>*<VB.?>*<NNP>+<NN>?}"""
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(pos)
        # print(chunked)
        is_chunk = False
        for subtree in chunked.subtrees(filter=lambda t: t.label() == "Chunk"):
            is_chunk = True
            # print(subtree)
        if not is_chunk:
            return None
        return chunked

    def chunk_to_question(self, chunk: Tree, corr: TextCorrelation):
        # remove chunk section and punction
        count = 0

        for subtree in chunk.subtrees(filter=lambda t: t.label() == "Chunk"):
            count = count + 1
        if count != 1:
            return None
        q = ""
        for subtree in chunk.subtrees(filter=lambda t: t.label() == "Chunk"):
            q = " ".join([w for w, t in subtree.leaves()]) + "?"
            chunk.remove(subtree)
        # assign rest as answer
        a = " ".join([w for w, t in subtree.leaves()])

        # create question obj
        bq = BaseQuestion(q, a, corr.yt_ts_link(), 1.0)  # TODO adjust confidence
        # return
        return bq

    def start(self):
        # no tf model or anything that requires starting
        pass

    def stop(self):
        # no tf model or anything that requires stopping
        pass

    def load_captions(self, captions):
        return super().load_captions(captions)

    def process_correlation(self, correlation: TextCorrelation):
        tokened = self.tokenize(correlation.caption)
        pos = self.pos_tag(tokened)
        chunked = self.subject_phrase(pos)
        if chunked is not None:
            return self.chunk_to_question(chunked, correlation)
        else:
            return None

    def generate_questions(self):
        if self.captions is None:
            logging.INFO("Attempted to generate questions without loading captions")
            return []
        # TODO
        return super().generate_questions()
