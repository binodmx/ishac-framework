import pickle
import client

with open('model.pkl', 'rb') as file:
  clf = pickle.load(file)

def predict(x, y):
    print(f"[INFO] Predicting access level...")
    y_pred = clf.predict_one(x)
    clf.learn_one(x, y)
    print(f"[INFO] Access level predicted")
    return y_pred

def validate(data):
    print(f"[INFO] Validating data: {data}")
    id = client.create_request("__ATTR_NAME__")
    attr_val = client.get_attribute(id)
    print(f"[INFO] Received attribute: {attr_val}")
    y_pred = predict(data["x"], data["y"])
    if data["y"] == 1:
        if y_pred == 1:
            return {"accessLevel":"GRANTED"}
        return {"accessLevel":"SUSPICIOUS"}
    else:
        if y_pred == 0:
            return {"accessLevel":"DENIED"}
        return {"accessLevel":"PENDING"}
