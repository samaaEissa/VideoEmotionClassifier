# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
import numpy as np


# initialising CNN
classifier=Sequential()

# step_1 Convelution layer
classifier.add(Convolution2D(64, 3,strides=3,input_shape = (64, 64, 3),
                             activation = 'relu'))

# step_2 pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Convolution2D(32, 5, strides=3, activation = 'relu',
                             padding='same'))
classifier.add(MaxPooling2D(pool_size = (2, 2),padding='same'))

 # Adding a third convolutional layer
classifier.add(Convolution2D(32, 5,strides=3, activation = 'relu',
                             padding='same'))
classifier.add(MaxPooling2D(pool_size = (2, 2),padding='same'))

#step_3 flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units=128 , activation='relu'))
classifier.add(Dense(units=7 , activation='softmax'))

# compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy',
                   metrics = ['accuracy'])


# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)




training_set = train_datagen.flow_from_directory('Emotions_training',
                                                 target_size = (48, 48),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('Emotions_testing',
                                            target_size = (48, 48),
                                            batch_size = 32,
                                            class_mode = 'categorical')
training_set.class_indices

classifier.fit_generator(training_set,
                         samples_per_epoch = 1098,
                         nb_epoch = 100,
                         validation_data = test_set,
                         nb_val_samples =273 )


#classifier.save('emotionalClassifier.h5')


# serialize model to JSON
model_json = classifier.to_json()
with open("emotionalClassifier.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
classifier.save_weights("emotionalClassifier.h5")
print("Saved model to disk")


# load json and create model
from keras.models import model_from_json

json_file = open('emotionalClassifier.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)




# # load weights into new model
# loaded_model.load_weights("emotionalClassifier.h5")
# print("Loaded model from disk")
# #Predicting single new observation
# new_prediction=model.predict(sc.transform(np.array([[0.0,0,600,1,40,30,60000,2,1,1,50000]])))
# new_prediction = (new_prediction > 0.5)