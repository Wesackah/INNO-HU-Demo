import json

from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import base64, os

import audio_converter
import backend_prediction
import wav_splitter

app = Flask(__name__)
UPLOAD_FOLDER = 'temp_upload'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        EmptyFolders()
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(UPLOAD_FOLDER, filename))
        audio_converter.convert(UPLOAD_FOLDER)
        wav_splitter.split_wav(os.path.join(UPLOAD_FOLDER, filename))
        emotions, badscore = backend_prediction.predict()
        JsonEmotions = json.dumps(emotions)
        return render_template("result.html", emotions=JsonEmotions, badvalues=badscore)
    badtest = {1: 0.2658739128383014, 2: 0.5424062308308527, 3: 0.8564104149701518, 4: 0.47276983485868906,
                5: 0.6748449524351346}
    emotions = {"chunk0": {"female_angry": 0.003969725, "male_angry": 0.23694685, "male_fearful": 0.023013767,
                           "male_happy": 0.73409116, "male_sad": 0.0019435697},
                "chunk1": {"female_angry": 0.0003118647, "female_happy": 0.00015557489, "male_angry": 0.16601905,
                           "male_fearful": 0.19517009, "male_happy": 0.4574199, "male_sad": 0.18090522},
                "chunk2": {"female_angry": 0.0075172554, "female_happy": 0.05306731, "male_angry": 0.8482935,
                           "male_happy": 0.09052235, "male_sad": 0.0005063273},
                "chunk3": {"female_angry": 0.011409758, "female_happy": 0.00096154725, "male_angry": 0.41289842,
                           "male_fearful": 0.039059103, "male_happy": 0.52626854, "male_sad": 0.00940254},
                "chunk4": {"female_angry": 0.059095614, "female_happy": 0.012637476, "male_angry": 0.09841791,
                           "male_fearful": 0.510204, "male_happy": 0.31251594, "male_sad": 0.0071274047}}
    jsonEmotions = json.dumps(emotions)
    return render_template("result.html", badvalues=badtest, emotions=jsonEmotions)
    # return "Error"


def EmptyFolders():
    fragsFolder = "temp_fragment"
    filesFolder = "temp_upload"
    for root, dirs, files in os.walk(fragsFolder):
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(filesFolder):
        for file in files:
            os.remove(os.path.join(root, file))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=False, use_reloader=False)
