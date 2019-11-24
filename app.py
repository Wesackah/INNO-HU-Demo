import json

from flask import Flask,render_template,jsonify,request
from werkzeug import secure_filename
import base64,os

import audio_converter
import backend_prediction
import wav_splitter

app = Flask(__name__)
UPLOAD_FOLDER='temp_upload'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results",methods=['GET','POST'])
def results():
    if request.method == 'POST':
        EmptyFolders()
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(UPLOAD_FOLDER, filename))
        audio_converter.convert(UPLOAD_FOLDER)
        wav_splitter.split_wav(os.path.join(UPLOAD_FOLDER, filename))
        emotionvalues, badscore = backend_prediction.predict()
        return render_template("img.html", badvalues=badscore, emotions=emotionvalues)
        # return render_template("test.html", badvalues=badscore, emotions=emotionvalues)
    return "Error"



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
    app.run(host="0.0.0.0",port=5000,debug=True,threaded=False,use_reloader=False)
