# =========================
# 1. IMPORT LIBRARIES
# =========================
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# =========================
# 2. LOAD DATASET
# =========================
data = pd.read_csv("C:/Users/lovel/OneDrive/Desktop/new/dataset/cardio.csv")  # comma-separated CSV
data.columns = data.columns.str.strip()  # remove extra spaces in column names

print("Dataset Loaded Successfully ✅")
print(data.head())
print("\nColumns:", data.columns.tolist())

# =========================
# 3. DATA PREPROCESSING
# =========================
# Remove ID column if exists
if "id" in data.columns:
    data = data.drop("id", axis=1)

# Fill missing values with column mean
data = data.fillna(data.mean())

# Separate features and target
if "cardio" not in data.columns:
    raise KeyError("Column 'cardio' not found in dataset!")

X = data.drop("cardio", axis=1)
y = data["cardio"]

print("\nInput Shape:", X.shape)

# =========================
# 4. TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. FEATURE SCALING
# =========================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# =========================
# 6. BUILD ANN MODEL
# =========================
model = models.Sequential([
    layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(16, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# =========================
# 7. COMPILE MODEL
# =========================
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# =========================
# 8. TRAIN MODEL
# =========================
history = model.fit(
    X_train, y_train,
    epochs=5,
    batch_size=32,
    validation_data=(X_test, y_test)
)

# =========================
# 9. EVALUATE MODEL
# =========================
loss, accuracy = model.evaluate(X_test, y_test)
print("\nModel Accuracy:", accuracy)

# =========================
# 10. SAVE MODEL
# =========================
model.save("heart_ann_model.h5")
print("\nModel Saved Successfully 💾")

# =========================
# 11. USER INPUT PREDICTION
# =========================
print("\n🔽 Enter Patient Details 🔽")

def get_input(prompt, dtype=float, choices=None):
    while True:
        try:
            value = dtype(input(prompt))
            if choices and value not in choices:
                print(f"Invalid choice! Valid options: {choices}")
                continue
            return value
        except ValueError:
            print("Invalid input, try again!")

# Make sure input order matches dataset columns
user_data_dict = {}
for col in X.columns:
    if col == "gender":
        user_data_dict[col] = get_input(f"{col} (1=Male, 2=Female): ", int, [1,2])
    elif col in ["cholesterol", "gluc"]:
        user_data_dict[col] = get_input(f"{col} (1-Normal, 2-Above, 3-High): ", int, [1,2,3])
    elif col in ["smoke", "alco", "active"]:
        user_data_dict[col] = get_input(f"{col} (0=No, 1=Yes): ", int, [0,1])
    else:
        user_data_dict[col] = get_input(f"{col}: ")

# Convert to array
user_data = np.array([list(user_data_dict.values())])

# Scale input
user_data = scaler.transform(user_data)

# Predict
prediction = model.predict(user_data)

print("\nPrediction Value:", prediction[0][0])
if prediction[0][0] > 0.5:
    print("⚠️ Heart Disease Detected")
else:
    print("✅ No Heart Disease")