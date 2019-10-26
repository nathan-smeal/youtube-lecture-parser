from pytube import YouTube, Caption
import os

# YouTube('http://youtube.com/watch?v=9bZkp7q19f0').streams.first().download()


def capture_vid_captions(url: str, out_dir: str):
    yt = YouTube(url)
    title = yt.title
    c: YouTube.Caption

    caption = get_captions(yt)
    if caption is not None:
        out_path = os.path.join(out_dir, title)
        os.makedirs(out_path)
        srt_path = os.path.join(out_path, f"{title}.srt")
        with open(srt_path, "w") as srt_fp:
            srt_fp.write(caption.generate_srt_captions())

        vid = yt.streams.first().download()


def get_captions(yt: YouTube) -> Caption:
    captions = yt.captions.get_by_language_code("en")
    assert captions is not None
    # sort by length, we want to prefer non generated
    # we will use
    return captions.sort(key=lambda x: len(x.lang))[0]
