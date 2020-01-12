import numpy as np
import keras
import pickle
from sklearn.preprocessing import StandardScaler
from keras.preprocessing import image

with open('grayscaletrash_classifier', 'rb') as f:
    model = pickle.load(f)
img = image.load_img('request/images.jpg', grayscale = True,target_size = (128,128))
img = image.img_to_array(img)
img = np.expand_dims(img,axis=0)
prediction = model.predict(img)
if(prediction[0,0]==1):
    print('cardboard')
elif(prediction[0,1]==1):
    print('glass/plastic')
elif(prediction[0,2]==1):
    print('metal')
elif(prediction[0,3]==1):
    print('plastic/glass')
else:
    print('trash')
