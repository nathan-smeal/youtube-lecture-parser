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


def correlate_captions(
    caption_string: str, yt_link: str, combine_sent=True
) -> List[TextCorrelation]:
    """Generates a list of Text correlations with shifted timestamp

    Arguments:
        caption_string {str} -- Raw XML string (from caption obj usually)
        yt_link {str} -- youtube url for reference

    Returns:
        List[TextCorrelation] -- Correlated timestamp hints
    """
    subRips: List[SubRipItem] = pysrt.from_string(caption_string)
    # need to handle end time for caption combining
    result = [convert_subrip(s, yt_link) for s in subRips]

    # collapse correlations if needed
    if combine_sent:
        pass
    return result


def canCombineCaption(first: SubRipItem, second: SubRipItem, thresh=500) -> bool:
    # check if punctuation

    # check if start and end are close
    return totalTime(second.start.to_time()) - totalTime(first.end.to_time()) < thresh


def combine(corr1: TextCorrelation, corr2: TextCorrelation) -> TextCorrelation:
    first = corr1 if corr1.timestamps < corr2.timestamps else corr2
    second = corr1 if corr1.timestamps > corr2.timestamps else corr2

    return TextCorrelation(
        first.caption + second.caption, first.yt_link, first.timestamps
    )


def totalTime(time: datetime.time):
    return (
        time.hour * 3600 * 1000
        + time.minute * 60000
        + time.second * 1000
        + time.microsecond / 1000
    )


def convert_subrip(s: SubRipItem, yt_link: str, shift_ms=2000) -> TextCorrelation:

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

    captions = correlate_captions(raw_caption, yt_link)

    return raw_caption, captions
