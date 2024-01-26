import pickle
from river import stream, tree
import client
import time

# threshold = 0.77

with open('../model.pkl', 'rb') as file:
  clf = pickle.load(file)

with open('../label_encoders.pkl', 'rb') as file:
    label_encoders = pickle.load(file)

def encode(x):
    print(f"[INFO] Encoding data: {x}")
    for key in x.keys():
        x[key] = label_encoders[key].fit_transform(x[key])
    print(f"[INFO] Encoded data: {x}")
    return x

def predict(x, y):
    print(f"[INFO] Predicting for data: {x}, {y}")
    encoded_x = encode(x)
    y_pred = clf.predict_one(encoded_x)
    clf.learn_one(encoded_x, y)
    # y_prob = clf.predict_proba_one(encoded_x)
    # if y_prob > threshold and y_pred != y:
    #     return y_pred
    # return y
    return y_pred

def validate(data):
    print(f"[INFO] Validating data: {data}")
    id = client.create_request("__ATTR_NAME__")
    attr_val = client.get_attribute(id)
    print(f"[INFO] Received attribute: {attr_val}")
    x = data["x"]
    y = data["y"]
    print(f"[INFO] Predicting access level...")
    # y_pred = predict(x, y)
    # if y == 1:
    #     if y_pred == 1:
    #         return {"accessLevel":"GRANTED"}
    #     return {"accessLevel":"SUSPICIOUS"}
    # else:
    #     if y_pred == 0:
    #         return {"accessLevel":"DENIED"}
    #     return {"accessLevel":"PENDING"}
