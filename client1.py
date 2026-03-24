# =========================
# 1. IMPORT LIBRARIES
# =========================
import flwr as fl
import tensorflow as tf
import numpy as np
import sys
import os
import numpy as np
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

import tensorflow as tf
from tensorflow.keras import layers, models

# =========================
# 2. LOAD DATASET
# =========================
#data = pd.read_csv("C:/Users/lovel/OneDrive/Desktop/fed pro/client/client1/hos3.csv")
#data = pd.read_csv("C:/Users/lovel/OneDrive/Desktop/fed pro/client/client1/hos1.csv")
#data = pd.read_csv ("C:/Users/lovel/OneDrive/Desktop/fed pro/client/client1\hos2.csv")
data =  pd.read_csv ("C:/Users/lovel/OneDrive/Desktop/fed pro/client/client1/hos4.csv")

# =========================
# 3. CLEAN + PREPROCESS
# =========================
data.columns = data.columns.str.strip()

# 🔥 Convert data_quality (VERY IMPORTANT)
data["data_quality"] = data["data_quality"].map({
    "good": 1.0,
    "medium": 0.5,
    "corrupted": 0.1
}).fillna(0.3)

data_quality_score = data["data_quality"].mean()

# FEATURES & LABEL
X = data.drop(["label_disease", "hospital"], axis=1)
y = data["label_disease"]

# =========================
# 4. TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. NORMALIZATION
# =========================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================
# 6. BUILD MODEL
# =========================
model = models.Sequential([
    layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# =========================
# 7. TRAIN MODEL
# =========================
model.fit(X_train, y_train, epochs=5, batch_size=16, verbose=0)

# =========================
# 8. PREDICTIONS
# =========================
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int)

# =========================
# 9. ACCURACY
# =========================
accuracy = accuracy_score(y_test, y_pred)

# =========================
# 10. ENTROPY
# =========================
def entropy(p):
    p = np.clip(p, 1e-10, 1 - 1e-10)
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

entropy_values = entropy(y_pred_prob)
avg_entropy = np.mean(entropy_values)

# =========================
# 11. TRUST CALCULATION (UPDATED 🔥)
# =========================
T_old = 0.8

# combine accuracy + data quality
T_new = 0.5 * accuracy + 0.3 * data_quality_score + 0.2 * T_old

# =========================
# 12. RELIABILITY
# =========================
alpha = 0.6
#R = alpha * T_new + (1 - alpha) * (1 - avg_entropy)
R = 0.7 * T_new + 0.3 * (1 - avg_entropy)

# =========================
# 13. EXPLANATION OUTPUT 🔥🔥🔥
# =========================
print("\n========= CLIENT TRUST ANALYSIS =========")

print("\n--- Step 1: Accuracy ---")
print(f"Model Accuracy = {accuracy:.4f}")

print("\n--- Step 2: Data Quality ---")
print(f"Data Quality Score = {data_quality_score:.4f}")

print("\n--- Step 3: Previous Trust ---")
print(f"Old Trust (T_old) = {T_old}")

print("\n--- Step 4: Trust Calculation Formula ---")
print("T_new = 0.5*(Accuracy) + 0.3*(Data Quality) + 0.2*(Old Trust)")

print("\n--- Step 5: Substitution ---")
print(f"T_new = 0.5*{accuracy:.4f} + 0.3*{data_quality_score:.4f} + 0.2*{T_old}")

print("\n--- Step 6: Final Trust ---")
print(f"T_new = {T_new:.4f}")

print("\n--- Step 7: Entropy ---")
print(f"Average Entropy = {avg_entropy:.4f}")

print("\n--- Step 8: Reliability Formula ---")
print("R = 0.6*(Trust) + 0.4*(1 - Entropy)")

print("\n--- Step 9: Substitution ---")
print(f"R = 0.6*{T_new:.4f} + 0.4*(1 - {avg_entropy:.4f})")

print("\n--- Step 10: Final Reliability ---")
print(f"R = {R:.4f}")

# =========================
# 14. FINAL RESULT
# =========================
print("\n========= FINAL RESULT =========")

if R > 0.65:
    print("🟢 CLIENT STATUS: GOOD")
elif R > 0.50:
    print("🟡 CLIENT STATUS: SLIGHTLY GOOD")
elif R > 0.30:
    print("🟠 CLIENT STATUS: SUSPICIOUS")
else:
    print("🔴 CLIENT STATUS: BAD")
# =========================
# 15. SERVER SEND
# =========================
weights = model.get_weights()

client_update = {
    "weights": weights,
    "trust": T_new,
    "entropy": float(avg_entropy),
    "reliability": float(R)
}

print("\n📤 Data Ready to Send to Server")

# =========================
# CLASS
# =========================
class TrustClient(fl.client.NumPyClient):

    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)

        model.fit(X_train, y_train, epochs=3, batch_size=16, verbose=0)

        y_pred_prob = model.predict(X_test)
        y_pred = (y_pred_prob > 0.5).astype(int)

        acc = accuracy_score(y_test, y_pred)

        entropy_values = entropy(y_pred_prob)
        avg_ent = np.mean(entropy_values)

        T_new = 0.5 * acc + 0.3 * data_quality_score + 0.2 * T_old
        R = 0.7 * T_new + 0.3 * (1 - avg_ent)

        return model.get_weights(), len(X_train), {
            "trust": float(T_new),
            "entropy": float(avg_ent),
            "reliability": float(R)
        }

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, acc = model.evaluate(X_test, y_test, verbose=0)
        return loss, len(X_test), {"accuracy": float(acc)}


# =========================
# MAIN START
# =========================
if __name__ == "__main__":

    fl.client.start_numpy_client(
        server_address="192.168.1.6:8081",
        client=TrustClient()   # ✅ CORRECT
    )