# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: tf_test
#     language: python
#     name: tf_test
# ---

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from tensorflow.keras.optimizers import SGD, Adam
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

# +
"""
This function, as well as load_mnist_dataset, were both found on
pyimagesearch.com/2020/08/17/ocr-with-keras-tensorflow-and-deep-learning/
They are used to load the training/testing datasets for the ORC model
"""
def load_A_Z_dataset(datasetPath):
    data = []
    labels = []
    for row in open(datasetPath):
        row = row.split(",")
        
        label = int(row[0])

        image = np.array([int(x) for x in row[1:]], dtype="uint8")
        
        # images are represented as single channel (grayscale) images
        # that are 28x28=784 pixels -- we need to take this flattened
        # 784-d list of numbers and repshape them into a 28x28 matrix
        image = image.reshape((28, 28))
        
        # plt.imshow(image, cmap='gray')
        # break
        
        # update the list of data and labels
        data.append(image)
        labels.append(label)

    # convert the data and labels to NumPy arrays
    data = np.array(data, dtype="float32")
    labels = np.array(labels, dtype="int")
    # return a 2-tuple of the A-Z data and labels
    return (data, labels)
    
def load_mnist_dataset():
	# load the MNIST dataset and stack the training data and testing
	# data together (we'll create our own training and testing splits
	# later in the project)
	((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()
	data = np.vstack([trainData, testData])
	labels = np.hstack([trainLabels, testLabels])
	# return a 2-tuple of the MNIST data and labels
	return (data, labels)


A_Z_dataset = '/project/arcc-students/csloan5/OilWellCards_project/code/A-Z_dataset/A-Z_dataset.csv'

# Load the datasets
(azData, azLabels) = load_A_Z_dataset(A_Z_dataset)
(digitsData, digitsLabels) = load_mnist_dataset()


# +
# Make sure that labels don't overlap
azLabels+=10

# Combine the data and labels from both datasets
data = np.vstack([azData, digitsData])
labels = np.hstack([azLabels, digitsLabels])
# -

# Normalize the data
data = np.expand_dims(data, axis=-1)  # Add a single channel dimension
data /= 255.0

# +
labels = to_categorical(labels, num_classes = 36, dtype = 'int')
counts = labels.sum(axis=0)

# Calculate the weight for each character in the data
weights = {}

for i in range(0, len(counts)):
    weights[i] = counts.max() / counts[i]

# +
# Split the data and shuffle it.
(trainX, testX, trainY, testY) = train_test_split(data,\
	labels, test_size=0.20, stratify=labels, random_state=42)

# Print the shapes of the datasets
print(trainX.shape)
print(trainY.shape)
print(testX.shape)
print(testY.shape)
# -

# Create the network model
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(28,28,1)))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding = 'same'))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))
model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding = 'valid'))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))
model.add(Flatten())
model.add(Dense(64,activation ="relu"))
model.add(Dense(128,activation ="relu"))
model.add(Dense(36,activation ="softmax"))

# +
# Compile and fit the model
model.compile(optimizer = Adam(learning_rate=0.001),\
              loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(
    trainX,
    trainY,
    batch_size=32,
    validation_data=(testX, testY),
    epochs=20,
    #class_weight=weights,
    verbose=1)

# Save the model
model.summary()
model.save(r'first_CNN_OCR_model.h5')
print("Done")
# -


