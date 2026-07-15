import tensorflow as tf
from tensorflow.keras import layers, models

# 1. Download data automatically (Unit 1 & 2)
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# 2. Pre-process (Unit 3 Fundamentals)
x_train = x_train.reshape((60000, 28, 28, 1)).astype('float32') / 255
x_test = x_test.reshape((10000, 28, 28, 1)).astype('float32') / 255

# 3. Build CNN Architecture (Unit 2)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax') # 10 classes (0-9)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 4. Train the model
print("Training the CNN... please wait.")
model.fit(x_train, y_train, epochs=3, validation_data=(x_test, y_test))

# 5. Save the brain
model.save('digit_model.h5')
print("Model saved as 'digit_model.h5'. You can now run the Final Solver.")