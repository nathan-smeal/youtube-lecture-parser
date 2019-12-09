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
import string


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
    if not combine_sent:
        result = [convert_subrip(s, yt_link) for s in subRips]
    else:
        result = combine_subs(subRips, yt_link)

    # collapse correlations if needed
    print(result)
    return result


def combine_subs(subs: List[SubRipItem], yt_link: str):
    isubs = iter(subs)
    last_sub = next(isubs, -1)
    next_sub = next(isubs, -1)
    if next_sub == -1:
        return []
    last_corr = convert_subrip(next_sub, yt_link)
    result = []
    while next_sub != -1:

        next_corr = convert_subrip(next_sub, yt_link)
        if canCombineCaption(last_sub, next_sub):
            last_corr = combine(last_corr, next_corr)
        else:
            result.append(last_corr)
            last_corr = convert_subrip(next_sub, yt_link)

        last_sub = next_sub
        next_sub = next(isubs, -1)
    return result


def canCombineCaption(first: SubRipItem, second: SubRipItem, thresh=500) -> bool:
    # check if punctuation
    punc = [".", "?", "!"]
    eos = first.text.strip()[-1] in punc
    close_time = (
        totalTime(second.start.to_time()) - totalTime(first.end.to_time()) < thresh
    )
    # check if start and end are close
    # print(first.text.strip()[-1])
    # print(eos)
    # if not eos and close_time:
    #     print(first.text + "COMBINED WITH" + second.text)
    # print(close_time)
    return not eos and close_time


def combine(corr1: TextCorrelation, corr2: TextCorrelation) -> TextCorrelation:
    first = corr1 if corr1.timestamps < corr2.timestamps else corr2
    second = corr1 if corr1.timestamps > corr2.timestamps else corr2

    return TextCorrelation(
        first.caption + " " + second.caption, first.yt_link, first.timestamps
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
    if True:
        with open("current.srt", "w") as out:
            out.write(raw_caption)

    captions = correlate_captions(raw_caption, yt_link)

    return raw_caption, captions
