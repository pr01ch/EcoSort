import tensorflow as tf
import numpy as np

# Load the Keras model
model_path = "ai-model/e_waste_model.keras"
model = tf.keras.models.load_model(model_path)

def make_prediction(input_data):
    """Make predictions using the loaded model."""
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return prediction.tolist()
