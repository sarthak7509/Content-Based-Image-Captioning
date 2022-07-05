from ast import Global
import base64
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
import pickle
import os
from PIL import Image
import io
import flask
import werkzeug
import numpy as np
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from flask import render_template
import random
import os
app = Flask(__name__)
CORS(app)
Modal = None

def getModal():
    global Modal
    img_size =224
    Modal = ResNet50(weights='imagenet', include_top=False,input_shape=(img_size, img_size, 3),pooling='max')

getModal()

def caption(image):
    with open('utilities/engine_modal.pickle','rb') as f:
        neighbours = pickle.load(f)
    with open('utilities/filenames-coco2014.pickle','rb') as f:
        fileNames = pickle.load(f)
    with open('utilities\image_to_caption.pickle','rb') as f:
        image_path_to_caption = pickle.load(f)
    image = image.resize((224,224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    test_img_features = Modal.predict(preprocessed_img, batch_size=1)
    _, indices = neighbours.kneighbors(test_img_features)
    captions = image_path_to_caption[fileNames[indices[0][0]]]
    n = random.randint(0,len(captions)-1)
    return captions[n]




@app.route('/predict',methods=['POST'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    captions = caption(image)
    print(captions)
    response = {
        'label':captions,
    }

    return jsonify(response)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT',5000))
    app.run('0.0.0.0',PORT)