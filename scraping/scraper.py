from pytube import YouTube, Caption
import os
from logzero import logger
from correlator.correlator import correlate_video, Correlation
from typing import List


# YouTube('http://youtube.com/watch?v=9bZkp7q19f0').streams.first().download()


def capture_vid_captions(url: str, out_dir: str, title=None) -> List[Correlation]:
    yt = YouTube(url)
    # title = yt.title
    c: YouTube.Caption

    caption = get_captions(yt)
    if caption is not None:
        try:
            stream = yt.streams.first()
            title = title or stream.title
            out_path = os.path.join(out_dir, title)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            srt_path = os.path.join(out_path, f"{title}.srt")
            with open(srt_path, "w") as srt_fp:
                srt_fp.write(caption.generate_srt_captions())
            out_fp = stream.download(output_path=out_path, filename=f"{title}")
            logger.info(out_fp)
            # TODO actually utilize these results
            logger.info("Correlations next")
            return correlate_video(out_fp, srt_path, url)
            # with open(mp4_path, "w") as mp4_fp:
            #     mp4_fp.write(vid)
        except IOError as e:
            logger.error(e)
            return []

    return []


def get_captions(yt: YouTube) -> Caption:
    captions = list(yt.captions.all())
    # print(type(captions))
    assert captions is not None and isinstance(
        captions, list
    ), f"Captions is: {type(captions)}"
    for c in captions:
        # ignore autogenerated for now
        if c.name.lower() == "english":
            return c
        print(c)
    # ok something went wrong
    raise ValueError("The passed youtube object didn't have manual english subtitles")
    # sort by length, we want to prefer non generated
    # we will use
    # return [x.name.lower() == "english" for x in captions][0]

    # for some reason filter doens't work with this list object.
    # I have to assume captions is actually a weird query object that is emulating a list without implementing it
    # return captions.filter(lambda x: x.name.lower() == "english")[0]
