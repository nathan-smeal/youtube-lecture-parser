from typing import List, Tuple
from .text_correlation import TextCorrelation
from logzero import logger
from pytube import YouTube, Caption
from scraping.scraper import get_captions
import pysrt
from pysrt.srttime import SubRipTime
from pysrt.srtitem import SubRipItem
from pysrt.srtfile import SubRipFile
import datetime


def correlate_captions(caption_string: str, yt_link: str) -> List[TextCorrelation]:
    """Generates a list of Text correlations with shifted timestamp

    Arguments:
        caption_string {str} -- Raw XML string (from caption obj usually)
        yt_link {str} -- youtube url for reference

    Returns:
        List[TextCorrelation] -- Correlated timestamp hints
    """
    subRips: List[SubRipItem] = pysrt.from_string(caption_string)
    result = [convert_subrip(s, yt_link) for s in subRips]

    return result


def convert_subrip(s: SubRipItem, yt_link: str, shift_ms=2000) -> TextCorrelation:
    def totalTime(time: datetime.time):
        return (
            time.hour * 3600 * 1000
            + time.minute * 60000
            + time.second * 1000
            + time.microsecond / 1000
        )

    time_ms = totalTime(s.start.to_time())
    shifted = time_ms - shift_ms
    shifted = shifted if shifted > 0.0 else 0.0
    return TextCorrelation(s.text, yt_link, shifted)


def captions_link(yt_link: str) -> Tuple[str, List[TextCorrelation]]:
    """This method takes in a youtube link and generates list of captions from yt.  No files generated

    Arguments:
        yt_link {str} -- Youtube URL;  Must have captions

    Returns:
        List[TextCorrelation] -- Parsed captions
    """
    yt = YouTube(yt_link)
    c: Caption
    c = get_captions(yt)

    raw_caption = c.generate_srt_captions()
    pysrt.from_string
    captions = correlate_captions(raw_caption, yt_link)

    return raw_caption, captions
