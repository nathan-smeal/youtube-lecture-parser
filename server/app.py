from logzero import logging
from flask import Flask, request, jsonify, render_template, send_file, Response
from correlator.caption_ts_correlator import captions_link
from q_generator.pos_model import PosModel
from q_generator.popo import BaseQuestion

app = Flask(__name__)
_VERSION = 1  # API version


@app.route("/v{}/generate".format(_VERSION), methods=["POST"])
def q_generate():
    try:
        url = request.json["yt_url"]
        if "tube" in url:
            # TODO:  This should
            raw, corrs = captions_link(url)
            m = PosModel()
            qs = m.q_from_c(corrs, raw)
            return jsonify({"cards": qs})
        else:
            return jsonify({"error": "only youtube links files, please"})
    except Exception as _:
        logging.error(_)
        return jsonify({"error": "Did you mean to send: {'yt_url': 'some_jpeg_url'}"})


if __name__ == "__main__":
    app.run()
