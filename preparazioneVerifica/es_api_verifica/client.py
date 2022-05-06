import requests
import random
import time

ID = 2

while True:
    data = requests.get(f"http://localhost:5000/operation?id={ID}").json()
    operation = data["data"][0][1]
    id = data["data"][0][0]
    
    if len(data["data"][0]) == 0:
        print("non ci sono più operazioni da fare")
        break
    else:
        value = eval(operation)
        print(f"operazione svolta dali client n{ID}")

        requests.get(f"http://localhost:5000/response?idOp={id}&ris={value}")
    time.sleep(random.randint(1,5))