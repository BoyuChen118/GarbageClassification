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

classifier = Sequential()
#32 conv filter each filter is 3*3
classifier.add(Convolution2D( 32,(3,3), input_shape = (128,128,3), activation = 'relu'))#convolution
# classifier.add(Convolution2D( 32,(3,3), activation = 'relu'))
#Pooling
classifier.add(MaxPooling2D(pool_size=(2,2)))

#second/third conv layer


classifier.add(Convolution2D( 64, (3,3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
classifier.add(Convolution2D(128, (3,3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size=(2,2)))
#flatten into an array
classifier.add(Flatten())
#ANN
classifier.add(Dense(units = 128, activation ='relu'))
classifier.add(Dense(units = 2, activation = 'softmax'))
classifier.compile(optimizer = 'adam', loss='categorical_crossentropy', metrics=['accuracy'])

#fitting the images
from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(
        'dataset/training_set',
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical')

validation_set = test_datagen.flow_from_directory(
        'dataset/test_set',
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical')

classifier.fit_generator(
        training_set,
        steps_per_epoch=8000/32,
        epochs=5,
        validation_data=validation_set,
        validation_steps=2000/32) #validation steps= # of images in test sample
# import pickle
# with open('cat_dog_predictor(v2)', 'wb') as f:
#     pickle.dump(classifier,f)
from keras.preprocessing.image import load_img
import numpy as np
from keras.preprocessing import image
img = image.load_img('requests/cattest.jpg', target_size=(128,128))
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
fin=classifier.predict(img)
print(fin)