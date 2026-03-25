import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("🚀 Federated Learning with Hospital Dataset\n")

# =========================
# 1. LOAD DATASET
# =========================
data = pd.read_csv("C:/Users/lovel/OneDrive/Desktop/linked in/cardio.csv")

# Target column (important)
X = data.drop("cardio", axis=1)
y = data["cardio"]

# =========================
# 2. TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 3. DATA SCALING (IMPORTANT FIX)
# =========================
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================
# 4. SPLIT INTO 2 CLIENTS
# =========================
mid = len(X_train) // 2

client1_X = X_train[:mid]
client1_y = y_train[:mid]

client2_X = X_train[mid:]
client2_y = y_train[mid:]

# =========================
# 5. LOCAL TRAINING
# =========================
model1 = LogisticRegression(max_iter=3000)
model2 = LogisticRegression(max_iter=3000)

model1.fit(client1_X, client1_y)
model2.fit(client2_X, client2_y)

# =========================
# 6. CLIENT ACCURACY
# =========================
pred1 = model1.predict(X_test)
pred2 = model2.predict(X_test)

acc1 = accuracy_score(y_test, pred1)
acc2 = accuracy_score(y_test, pred2)

print("📊 Client 1 Accuracy:", round(acc1, 3))
print("📊 Client 2 Accuracy:", round(acc2, 3))

# =========================
# 7. FEDERATED AVERAGING
# =========================
w1 = model1.coef_
w2 = model2.coef_

global_weights = (w1 + w2) / 2
global_intercept = (model1.intercept_ + model2.intercept_) / 2

# =========================
# 8. GLOBAL MODEL
# =========================
global_model = LogisticRegression(max_iter=3000)

# Fit once to initialize
global_model.fit(X_train, y_train)

# Replace weights
global_model.coef_ = global_weights
global_model.intercept_ = global_intercept

# =========================
# 9. GLOBAL ACCURACY
# =========================
global_pred = global_model.predict(X_test)
global_acc = accuracy_score(y_test, global_pred)

print("\n🌍 Global Model Accuracy:", round(global_acc, 3))

print("\n✅ Federated Learning Completed Successfully!")