import re
import srt

# ts_pattern = "(^\d+$)|(^\d{2}:\d{2}:\d{2},\d{3}.*\d{2}:\d{2}:\d{2},\d{3}$)"


def remove_time_stamps(input_str: str):
    # reg_obj = re.compile(ts_pattern, re.IGNORECASE)
    subs = srt.parse(input_str)
    output = " ".join([x.content for x in subs])
    return output
