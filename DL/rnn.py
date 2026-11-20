# Simple RNN: movie review sentiment (IMDB)
from tensorflow import keras
from tensorflow.keras import layers

words, maxlen = 10000, 200
(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(num_words=words)
x_train = keras.utils.pad_sequences(x_train, maxlen=maxlen)
x_test = keras.utils.pad_sequences(x_test, maxlen=maxlen)

model = keras.Sequential([
    keras.Input(shape=(maxlen,)),
    layers.Embedding(words, 32),
    layers.SimpleRNN(32),
    layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.summary()
model.fit(x_train, y_train, epochs=3, batch_size=64, validation_split=0.2, verbose=2)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print("Test accuracy:", round(acc, 4))
p = model.predict(x_test[:5], verbose=0).ravel()
print("Predicted:", (p > 0.5).astype(int), "Actual:", y_test[:5])
