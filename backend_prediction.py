import pandas as pd
import librosa
import librosa.display
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from keras.models import model_from_json
from sklearn.preprocessing import LabelEncoder
import os

#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
def predict():

    pred_to_class = {
    0: "female_angry",
    1: "female_calm",
    2: "female_fearful",
    3: "female_happy",
    4: "female_sad",
    5: "male_angry",
    6: "male_calm",
    7: "male_fearful",
    8: "male_happy",
    9: "male_sad"
}
    badValDict = {}
    allEmotionDict = {}
    bad_val = 0
    bad_array = [0, 2, 4, 5, 7, 9]
    iteration = 1
    Model_filename = 'models/Emotion_Voice_Detection_Model.h5'
    json_file = open('models/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(Model_filename)

    for (dirpath, dirnames, filenames) in os.walk("temp_fragment/"):
        for file_name in filenames:
            allEmotionDict["chunk"+str(iteration)] = {}
            X, sample_rate = librosa.load(os.path.join(dirpath,file_name),
                                          res_type='kaiser_fast',
                                          duration=2.5,
                                          sr=22050 * 2,
                                          offset=0.50)
            sample_rate = np.array(sample_rate)
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13), axis=0)
            livedf2 = pd.DataFrame(data=mfccs)
            livedf3 = livedf2.stack().to_frame().T
            twodim = np.expand_dims(livedf3, axis=2)

            preds = loaded_model.predict(twodim,
                                         batch_size=32,
                                         verbose=1)
            for i in range(0, len(preds[0])):

                if i in bad_array:
                    bad_val = bad_val + preds[0][i]
                if preds[0][i] * 100 > 0.1:
                    allEmotionDict["chunk"+str(iteration)][pred_to_class[i]] = str(preds[0][i])

            badValDict[iteration] = bad_val
            bad_val = 0
            iteration = iteration + 1
        return allEmotionDict, badValDict







