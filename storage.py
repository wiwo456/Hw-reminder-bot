import json

def load_storage():
    with open ("storage.json", "r")as f:
        data = json.load(f)
    return data 

def save_storage(storage_data):
    with open("storage.json", "w") as f:
        json.dump(storage_data, f, indent = 4)