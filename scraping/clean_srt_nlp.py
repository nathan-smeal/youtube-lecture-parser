import re
import srt


def remove_time_stamps(input_str: str):
    subs = srt.parse(input_str)
    output = " ".join([x.content for x in subs])
    return output
