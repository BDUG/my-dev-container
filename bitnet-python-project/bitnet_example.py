import tensorflow as tf

# 🧩 Custom binary activation mit STE
@tf.custom_gradient
def binary_activation(x):
    y = tf.sign(x)
    def grad(dy):
        return dy  # Straight-Through Estimator
    return y, grad

class BinaryActivation(tf.keras.layers.Layer):
    def call(self, inputs):
        return binary_activation(inputs)

# 🧩 Dense-Layer mit binären Gewichten
class BinaryDense(tf.keras.layers.Layer):
    def __init__(self, units):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        initializer = tf.keras.initializers.RandomNormal(stddev=0.1)
        self.w = self.add_weight(shape=(input_shape[-1], self.units),
                                 initializer=initializer,
                                 trainable=True)

    def call(self, inputs):
        w_bin = tf.sign(self.w)
        x_bin = tf.sign(inputs)
        return tf.matmul(x_bin, w_bin)

# 📐 Einfaches BitNet-Modell
def build_bitnet():
    inputs = tf.keras.Input(shape=(28*28,))
    x = BinaryDense(256)(inputs)
    x = BinaryActivation()(x)
    x = BinaryDense(256)(x)
    x = BinaryActivation()(x)
    x = tf.keras.layers.Dense(10, activation='softmax')(x)  # Klassische Ausgabe
    return tf.keras.Model(inputs, x)

# 🔢 MNIST vorbereiten
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

# 🏗️ Modell erstellen und trainieren
model = build_bitnet()
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=64, epochs=3, validation_split=0.1)

# 🧪 Testen
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)
