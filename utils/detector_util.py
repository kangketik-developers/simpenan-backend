import os, cv2
import numpy as np

from tensorflow import keras

BASE_PATH = os.path.abspath(os.path.dirname("."))
TF_MODEL_DIR = os.path.join(BASE_PATH, "assets", "tf_trained_model", "latest")

def detect(labels, target):
    if os.path.exists(TF_MODEL_DIR):
        model = keras.models.load_model(TF_MODEL_DIR)
        img = cv2.imread(target)
        imgr = cv2.resize(img, (200, 200))
        imgrgb = cv2.cvtColor(imgr, cv2.COLOR_BGR2RGB)
        final_format = np.array([imgrgb]).astype('float64') / 255.0
        pred = model.predict(final_format)
        index = np.argmax(pred[0])
        prob = np.max(pred[0])
        label = labels[index]
        result = "Predicted : {} {:.2f}%".format(label, prob*100)
        return [label, round(prob*100, 2), result]