# bitnet_tvm_qonnx_export.py
# Final version: QKeras + Functional API + eager-compatible ONNX export for ARM NEON

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from qkeras import QDense, quantized_bits
from qonnx.core.modelwrapper import ModelWrapper
import tf2onnx
import onnx
import tvm
from tvm import relay
from tvm.contrib import graph_executor
import numpy as np

# Load MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28 * 28).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28 * 28).astype("float32") / 255.0
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# Functional API model with named input/output
def build_model():
    inputs = tf.keras.Input(shape=(28*28,), name="input_1")
    x = QDense(256, kernel_quantizer=quantized_bits(1, 0, 1),
               bias_quantizer=quantized_bits(1, 0, 1), name="qdense1")(inputs)
    x = tf.keras.layers.Activation("relu")(x)
    x = QDense(256, kernel_quantizer=quantized_bits(1, 0, 1),
               bias_quantizer=quantized_bits(1, 0, 1), name="qdense2")(x)
    x = tf.keras.layers.Activation("relu")(x)
    outputs = tf.keras.layers.Dense(10, activation="softmax", name="output")(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs, name="bitnet_model")

# Build and train model
model = build_model()
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"], run_eagerly=True)
model.fit(x_train, y_train_cat, epochs=2, batch_size=128, validation_split=0.1)

# Save HDF5 model (optional)
model.save("qbitnet_model.h5")

# Export ONNX using from_function to preserve eager execution
@tf.function(input_signature=[tf.TensorSpec([None, 784], tf.float32, name="input_1")])
def model_func(x):
    return {"output": model(x)}

input_signature = [tf.TensorSpec([None, 784], tf.float32, name="input_1")]
model_proto, _ = tf2onnx.convert.from_function(
    model_func,
    opset=13,
    output_path="qbitnet_model.onnx", input_signature=input_signature
)

# Wrap with QONNX
model_wrapped = ModelWrapper("qbitnet_model.onnx")
model_wrapped.save("qbitnet_model_qonnx.onnx")

# Load and convert ONNX to Relay
onnx_model = onnx.load("qbitnet_model_qonnx.onnx")
shape_dict = {"input_1": (1, 784)}
mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

# Compile for ARM Cortex-A + NEON
target = tvm.target.Target("llvm -mtriple=armv7l-linux-gnueabihf -mcpu=cortex-a53 -mattr=+neon")
with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

# Save compiled shared object
lib.export_library("bitnet_tvm_deploy.so")

print("✅ Fully fixed QKeras → ONNX → TVM pipeline exported with eager compatibility.")
