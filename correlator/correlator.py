import cv2
import pysrt
import datetime
import time
import os
from correlator.correlation import Correlation
from typing import List
import pytesseract
from pytesseract import Output
from logzero import logger
import numpy as np

# import cv2


def correlate_video(input_vid, input_srt, yt_link) -> List[Correlation]:
    result = []
    cap = cv2.VideoCapture(input_vid)
    fps = cap.get(cv2.CAP_PROP_FPS)
    logger.info(input_vid)
    logger.info(input_srt)
    logger.info(yt_link)

    def totalTime(end_time: datetime.time):
        return (
            end_time.hour * 3600 * 1000
            + end_time.minute * 60000
            + end_time.second * 1000
            + end_time.microsecond / 1000
        )

    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

    calc_timestamps = [0.0]
    subs = pysrt.open(input_srt)
    # for sub in subs:
    #     print(sub)
    #  test : pysrt.SubRipItem..end
    isubs = iter(subs)
    # passtype:  pysrt.SubRipItem
    next_sub = next(isubs)
    mstime = totalTime(next_sub.end.to_time())
    # datetime.time.hou
    # print(next_sub.te)
    print(next_sub.end.to_time().microsecond * 1000)
    # print(time.mktime(next_sub.end))
    while cap.isOpened():
        frame_exists, curr_frame = cap.read()

        if frame_exists:
            calc_timestamps.append(calc_timestamps[-1] + 1000.0 / fps)

            if next_sub != -1 and abs(mstime - calc_timestamps[-1]) < 1000.0 / fps:
                print(f"found: {calc_timestamps[-1]}")

                img = curr_frame
                text = next_sub.text
                # perform OCR
                ocr_res = perform_ocr(img)

                current = Correlation(
                    caption=text,
                    ocr_boxes=ocr_res,
                    timestamps=calc_timestamps[-1],
                    frame=img,
                    yt_link=yt_link,
                )
                result.append(current)

                next_sub = next(isubs, -1)
                if next_sub != -1:
                    mstime = totalTime(next_sub.end.to_time())
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))

        else:
            break

    cap.release()

    return result


def perform_ocr(img: np.ndarray):
    d = pytesseract.image_to_data(img, output_type=Output.DATAFRAME)
    return d
