import tensorflow as tf
import numpy as np

# Generate some training data
X_train = np.array([1, 2, 3, 4, 5], dtype=float)
Y_train = 3 * X_train + 2

# Build the neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])  # One neuron in the hidden layer
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, Y_train, epochs=500)

# Use the trained model to predict for new values
X_new = np.array([5, 10], dtype=float)
Y_pred = model.predict(X_new)

print("Predictions for X =", X_new)
print("Predicted Y values:", Y_pred.flatten())
