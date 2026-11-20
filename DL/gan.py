# GAN: generate handwritten digits (MNIST) with dense layers
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

(x, _), _ = keras.datasets.mnist.load_data()
x = (x[:10000].reshape(-1, 784) / 127.5 - 1).astype("float32")  # scale to [-1, 1]
noise_dim, batch = 64, 128

G = keras.Sequential([keras.Input(shape=(noise_dim,)),
    layers.Dense(128, activation="relu"), layers.Dense(784, activation="tanh")])
D = keras.Sequential([keras.Input(shape=(784,)),
    layers.Dense(128, activation="relu"), layers.Dense(1, activation="sigmoid")])
D.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

gan = keras.Sequential([G, D])
gan.compile(optimizer="adam", loss="binary_crossentropy")

for step in range(1, 5001):
    D.trainable = True                       # 1) train discriminator
    real = x[np.random.randint(0, len(x), batch)]
    fake = G(np.random.normal(size=(batch, noise_dim))).numpy()
    d_loss, d_acc = D.train_on_batch(np.vstack([real, fake]),
                                     np.vstack([np.ones((batch, 1)), np.zeros((batch, 1))]))
    D.trainable = False                      # 2) train generator through frozen D
    g_loss = gan.train_on_batch(np.random.normal(size=(batch, noise_dim)), np.ones((batch, 1)))
    if step % 1000 == 0:
        print(f"Step {step}: D loss={d_loss:.3f} D acc={d_acc:.2f} G loss={g_loss:.3f}")

img = G.predict(np.random.normal(size=(1, noise_dim)), verbose=0).reshape(28, 28)
for row in img[::2]:                         # print generated digit as text art
    print("".join("#" if v > 0 else "." for v in row))
