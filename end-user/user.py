import requests
import time
import pandas as pd
import json

df_x = pd.read_csv('x.csv')
df_y = pd.read_csv('y.csv')
x = df_x.to_dict(orient='index')
y = df_y.to_dict(orient='index')

n = 10
print(f"[INFO] Sending {n} requests to the server...")
start = time.time()
for i in range(n):
    url = "http://localhost:5000/validate"
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"x": x[i], "y": y[i]["allowed"]})
    response = requests.post(url, headers=headers, data=payload)
    print(response.json())
end = time.time()
print(f"[INFO] Total time for {n} requests: {end - start}")
print(f"[INFO] Average time per request: {(end - start) / n}")
