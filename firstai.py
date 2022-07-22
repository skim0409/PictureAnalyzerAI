import os.path
import random

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

types = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)


x_train = x_train/255
x_test = x_test/255


model = Sequential()


model.add( Conv2D(64, (5,5), activation='relu', input_shape=(32,32,3)) )
model.add(MaxPooling2D(pool_size=(2,2)))
model.add( Conv2D(32, (5,5), activation = 'relu') )
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Flatten())
model.add(Dense(2000, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(500, activation='relu'))
model.add(Dense(10, activation='softmax'))

#Compile the model

model.compile(loss = 'categorical_crossentropy',
              optimizer = 'adam',
              metrics= ['accuracy'])

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
#Train the model
# hist = model.fit(x_train, y_train_one_hot,
#                  batch_size = 512,
#                  epochs = 11,
#                  validation_split = float(0.1),
#                  callbacks=[cp_callback])

os.listdir(checkpoint_dir)

model.load_weights(checkpoint_path)
acc = model.evaluate(x_test, y_test_one_hot)[1]
print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
#test the model with an example
from skimage.transform import resize
from skimage import io
print("airplane")
print("automobile")
print("bird")
print("cat")
print("deer")
print("dog")
print("frog")
print("horse")
print("ship")
print("truck")
print('Choose the image to test: ')
input = input()
imgtype = input.lower()
rand_int = random.randint(1,3)
test1 = io.imread('https://skim-cifar.s3.ca-central-1.amazonaws.com/' + imgtype + str(rand_int) + '.jpeg') #replace with the path to your image if you would like to test your own piture
finalimg = resize(test1, (32,32,3))
plt.imshow(finalimg)
plt.imshow(test1)
plt.show()



prediction = model.predict(np.array([finalimg]))
list_index = [0,1,2,3,4,5,6,7,8,9]
x = prediction


for i in range(10):
    for j in range(10):
        if x[0][list_index[i]] > x[0][list_index[j]]:
            temp = list_index[i]
            list_index[i] = list_index[j]
            list_index[j] = temp


print("prediction ranking")
print("-----------------")
for i in range(3):
    print(i+1,'.', types[list_index[i]], '|', round(prediction[0][list_index[i]] * 100, 2), '%')
print("_________________")