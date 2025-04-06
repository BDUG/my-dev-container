import tensorflow as tf
import numpy as np
import os

# 📦 Binary Activation mit STE
@tf.custom_gradient
def binary_activation(x):
    y = tf.sign(x)
    def grad(dy):
        return dy
    return y, grad

class BinaryActivation(tf.keras.layers.Layer):
    def call(self, inputs):
        return binary_activation(inputs)

# 🧩 Binäre Dense-Layer (Train-time binär, Export als float32)
class BinaryDense(tf.keras.layers.Layer):
    def __init__(self, units, use_bias=False):
        super().__init__()
        self.units = units
        self.use_bias = use_bias

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer=tf.keras.initializers.RandomNormal(stddev=0.1),
            trainable=True
        )
        if self.use_bias:
            self.b = self.add_weight(shape=(self.units,), initializer="zeros", trainable=True)

    def call(self, inputs):
        w_bin = tf.sign(self.w)
        x_bin = tf.sign(inputs)
        out = tf.matmul(x_bin, w_bin)
        if self.use_bias:
            out = out + self.b
        return out

# 🏗️ BitNet bauen
def build_bitnet():
    inputs = tf.keras.Input(shape=(28*28,), name="input")
    x = BinaryDense(256)(inputs)
    x = BinaryActivation()(x)
    x = BinaryDense(256)(x)
    x = BinaryActivation()(x)
    x = tf.keras.layers.Dense(10, activation="softmax", name="output")(x)
    return tf.keras.Model(inputs, x)

# 📊 Daten laden
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

# 🧠 Modell trainieren
model = build_bitnet()
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(x_train, y_train, batch_size=64, epochs=3, validation_split=0.1)

# 📈 Test
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)

# 💾 Export als SavedModel
saved_model_dir = "./saved_bitnet_model.h5"
model.save(saved_model_dir)

# 🔁 Konvertierung zu TFLite
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()

# 💽 Speichern
tflite_path = "bitnet_model.tflite"
with open(tflite_path, "wb") as f:
    f.write(tflite_model)

print(f"TFLite-Modell gespeichert als: {tflite_path}")
