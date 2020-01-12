#part 1 preparing data and building the CNN
import pickle
import keras
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D 
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator

data = pd.read_csv('nopaper.txt', sep=" ", header=None)
data.columns = ["filename", "id"]
datagen=ImageDataGenerator(rescale=1./255)
train_generator=datagen.flow_from_dataframe(dataframe=data, directory="datas/all", 
x_col="filename", y_col="id", class_mode="categorical",color_mode='grayscale', target_size=(128,128), batch_size=32)
valid_generator=datagen.flow_from_dataframe(dataframe=data, directory="datas/all", 
x_col="filename", y_col="id", class_mode="categorical",color_mode='grayscale',target_size=(128,128), batch_size=32)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(data,isinstance(data,(str)))
classifier = Sequential()
#32 conv filter each filter is 3*3
classifier.add(Convolution2D( 32,(3,3), input_shape = (128,128,1), activation = 'relu'))#convolution
# classifier.add(Convolution2D( 32,(3,3), activation = 'relu'))
#Pooling
classifier.add(MaxPooling2D(pool_size=(2,2)))

#second/third conv layer


classifier.add(Convolution2D( 64, (3,3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
# classifier.add(Convolution2D(128, (3,3), activation = 'relu'))
# classifier.add(MaxPooling2D(pool_size=(2,2)))
#flatten into an array
classifier.add(Flatten())
#ANN
classifier.add(Dense(units = 128, activation ='relu'))
classifier.add(Dense(units = 5, activation = 'softmax'))
classifier.compile(optimizer = 'adam', loss='categorical_crossentropy', metrics=['accuracy'])

STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
classifier.fit_generator(generator=train_generator,
                    steps_per_epoch=200,
                    validation_data=valid_generator,
                    validation_steps=40,
                    epochs=15)#validation steps= # of images in test sample

import pickle
with open('grayscaletrash_classifier', 'wb') as f:
    pickle.dump(classifier,f)
from keras.preprocessing.image import load_img
import numpy as np
from keras.preprocessing import image
img = image.load_img('request/cardboard_3.jpg', grayscale=True,target_size=(128,128))
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
fin=classifier.predict(img)
print(fin)