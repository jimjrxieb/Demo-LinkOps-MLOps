import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def train_model():
    """Train the ML task classifier model."""
    # Load data
    df = pd.read_csv("dataset/tasks.csv")
    texts = df["task"].astype(str).tolist()
    labels = df["category"].astype(str).tolist()

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)

    # Tokenize
    tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    X = pad_sequences(sequences, maxlen=20)

    # Build model
    model = Sequential(
        [
            Embedding(5000, 64),
            GlobalAveragePooling1D(),
            Dense(64, activation="relu"),
            Dense(len(set(labels)), activation="softmax"),
        ]
    )
    model.compile(
        loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )

    # Train
    model.fit(X, y, epochs=10, verbose=1)

    # Save
    model.save("classifier_model.h5")

    # Save label encoder and tokenizer manually if needed
    import pickle

    with open("tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)


if __name__ == "__main__":
    train_model()
