# CNN: classify handwritten digits (MNIST)
from tensorflow import keras
from tensorflow.keras import layers

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1) / 255.0
x_test = x_test.reshape(-1, 28, 28, 1) / 255.0

model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.summary()
model.fit(x_train, y_train, epochs=2, batch_size=128, validation_split=0.1, verbose=2)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print("Test accuracy:", round(acc, 4))
pred = model.predict(x_test[:5], verbose=0).argmax(axis=1)
print("Predicted:", pred, "Actual:", y_test[:5])
