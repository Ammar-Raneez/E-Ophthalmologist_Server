import sys
import os
import glob
import re
import tensorflow as tf
from .DRFunctions import DRFunctions

functions = DRFunctions()

scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath)
MODEL_PATH = os.path.join(scriptdir, 'densenet121ML.h5')
model = tf.keras.models.load_model(MODEL_PATH)
print('Model loaded')

def model_predict(image_path, model):
    image_array = functions.preprocess(image_path)
    y_pred = model.predict(image_array)
    y_pred = y_pred > 0.5
    y_pred = y_pred.astype(int).sum(axis=1) - 1
    return y_pred

def upload(image_path):        
    # Make prediction
    prediction = model_predict(image_path, model)
    # These are the prediction categories 
    CATEGORIES = ['No Diabetic Retinopathy', 'Mild', 'Moderate', 'Severe', 'Proliferative']
    
    # getting the prediction result from the categories
    result = CATEGORIES[int(round(prediction[0]))]
    
    # returning the result
    return result


# ### Running the main application
if __name__ == '__main__':
    upload(sys.argv[1])