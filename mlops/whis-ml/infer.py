import pickle

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

model = tf.keras.models.load_model("classifier_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)


def predict_category(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=20)
    prediction = model.predict(padded)[0]
    label = label_encoder.inverse_transform([prediction.argmax()])[0]
    confidence = prediction.max()
    return label, confidence
