import cv2
import pysrt
import datetime
import time
import os


def correlate_video(input_vid, input_srt, slide):
    cap = cv2.VideoCapture(input_vid)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # TODO: combine several caption images into 1 if they are similar enough
    # meaning if they earlier image matches enough.... then combine.  idk that's a little touhg
    # really intesting problem though

    # TODO: also take the text and text multiline, handle the longer ones.

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 435)
    fontScale = 0.75
    fontColor = (0, 0, 255)
    lineType = 2
    bot_second = (10, 460)
    # max_char = 50
    # line_height = 25

    print(fps)

    def totalTime(end_time: datetime.time):
        return (
            end_time.hour * 3600000
            + end_time.second * 1000
            + end_time.microsecond / 1000
        )

    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    calc_timestamps = [0.0]
    subs = pysrt.open(input_srt)
    for sub in subs:
        print(sub)
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
            # print(mstime)
            # print(cap.get(cv2.CAP_PROP_POS_MSEC))
            # print(abs(mstime - cap.get(cv2.CAP_PROP_POS_MSEC)))
            # if len(timestamps) == 30:
            #     exit(1)
            calc_timestamps.append(calc_timestamps[-1] + 1000 / fps)
            if next_sub != -1 and abs(mstime - calc_timestamps[-1]) < fps:
                print("Found")
                img = curr_frame
                text = next_sub.text
                if len(next_sub.text) > 50:
                    split_i = next_sub.text[:50].rfind(" ")
                    next_line = text[split_i:]
                    text = text[:split_i]
                img = cv2.putText(
                    img,
                    text,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType,
                )
                if len(next_sub.text) > 50:
                    img = cv2.putText(
                        img, next_line, bot_second, font, fontScale, fontColor, lineType
                    )
                cv2.imwrite(f"./output/Slide_{slide}.png", img)
                # slide += 1
                # cv2.imshow("img",img)
                # cv2.waitKey(0)
                next_sub = next(isubs, -1)
                if next_sub != -1:
                    mstime = totalTime(next_sub.end.to_time())
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))

        else:
            break

    cap.release()

    # for i, (ts, cts) in enumerate(zip(timestamps, calc_timestamps)):
    #     print('Frame %d difference:'%i, abs(ts - cts))


def correlate_udacity(input_dir_vid, input_dir_srt):
    vs = os.listdir(input_dir_vid)
    s_v = {}
    for s in os.listdir(input_dir_srt):
        s_n = s.split("-")[0]
        for v in vs:
            if v.startswith(s_n):
                s_v[s] = v
                break
    slide = 1
    for s, v in s_v.items():
        input_srt = os.path.join(input_dir_srt, s)
        input_vid = os.path.join(input_dir_vid, v)
        correlate_video(input_vid, input_srt, slide)
        slide = slide + 1
