import requests
import time

n = 10

print(f"[INFO] Sending {n} requests to the server...")
start = time.time()
for i in range(n):
    requests.get("http://localhost:5000")
end = time.time()
print(f"[INFO] Total time for {n} requests: {end - start}")
print(f"[INFO] Average time per request: {(end - start) / n}")
