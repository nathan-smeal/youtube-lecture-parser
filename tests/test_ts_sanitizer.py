"""Tests for the srt sanitizer, namely timestamps.
"""
from scraping import clean_srt_nlp


class TestTimeStampSanitizer:
    def test_remove_timestamps(self):
        assert 1 == 1
        expected = "at the University of Iowa."
        input_str = """1
00:00:11,940 --> 00:00:13,740
at the University of Iowa."""
        actual = clean_srt_nlp.remove_time_stamps(input_str)
        assert expected == actual, f"{expected} does not equal {actual}"
