import argparse
import pickle
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
import numpy as np
from colored import fg
import random

color = fg('blue')
print(color + f'Loading model')

img_size =224
model = ResNet50(weights='imagenet', include_top=False,input_shape=(img_size, img_size, 3),pooling='max')

color = fg('green')
print(color + f'model loaded')

parser = argparse.ArgumentParser(description='Image for generating caption')
parser.add_argument('--image',metavar='-i',help='Path to the image ')

with open('utilities/engine_modal.pickle','rb') as f:
    neighbours = pickle.load(f)
with open('utilities/filenames-coco2014.pickle','rb') as f:
    fileNames = pickle.load(f)
with open('utilities\image_to_caption.pickle','rb') as f:
    image_path_to_caption = pickle.load(f)
args = parser.parse_args()
img_path = args.image
input_shape = (224, 224, 3)
img =  tf.keras.preprocessing.image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
img_array =  tf.keras.preprocessing.image.img_to_array(img)
expanded_img_array = np.expand_dims(img_array, axis=0)
preprocessed_img = preprocess_input(expanded_img_array)
test_img_features = model.predict(preprocessed_img, batch_size=1)

_, indices = neighbours.kneighbors(test_img_features)

print('/'*100)
captions = image_path_to_caption[fileNames[indices[0][0]]]
n = random.randint(0,len(captions))
print(captions[n])