import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pickle
import os
import base64
from datetime import datetime

def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    today = datetime.now().date()
    print("We are here:",today)
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    
    serialized_data = pickle.dumps(df)                    # bytes
    return base64.b64encode(serialized_data).decode("ascii")  # JSON-safe string

def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled clustered data.
    """
    # decode -> bytes -> DataFrame
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    clustering_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    # bytes -> base64 string for XCom
    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan.fit(df_scaled)

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, filename)
    with open(model_path, "wb") as f:
        pickle.dump(dbscan, f)
    
    # Save scaler (needed for preprocessing new data)
    scaler_path = os.path.join(output_dir, filename.replace('.pkl', '_scaler.pkl'))
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    return {"n_clusters": len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)}


def load_model_elbow(filename: str, sse: list):
    """
    Loads DBSCAN model and predicts cluster label for test.csv.
    Note: DBSCAN doesn't have a true predict method. This function uses fit_predict
    which refits the model on the new data. For proper prediction, you'd need to
    implement a custom approach using nearest neighbors to the core samples.
    """
    model_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    scaler_path = os.path.join(os.path.dirname(__file__), "../model", filename.replace('.pkl', '_scaler.pkl'))
    
    loaded_model: DBSCAN = pickle.load(open(model_path, "rb"))
    scaler: StandardScaler = pickle.load(open(scaler_path, "rb"))

    print("DBSCAN model loaded. Clusters found:",
          len(set(loaded_model.labels_)) - (1 if -1 in loaded_model.labels_ else 0))

    # Load and preprocess test data the same way as training data
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    # Assuming test.csv has the same columns as training data
    # If test.csv has different structure, adjust accordingly
    if "BALANCE" in df.columns and "PURCHASES" in df.columns and "CREDIT_LIMIT" in df.columns:
        test_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]
    else:
        test_data = df
    
    # Preprocess test data with the same scaler
    test_data_scaled = scaler.transform(test_data)
    
    # Note: fit_predict refits the model. For a single prediction, we take the first result
    # This is not ideal but DBSCAN doesn't support prediction on new data directly
    pred = loaded_model.fit_predict(test_data_scaled)[0]
    print(int(pred))

    if pred == -1:
        print("⚠️ Sample considered an outlier")
    return int(pred)


