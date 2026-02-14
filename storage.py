#this is the storage of the assignments 
import json


def load_storage():
    try:
        with open("storage.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"reminded_hw": []}


def save_storage(storage_data):
    with open("storage.json", "w") as f:
        json.dump(storage_data, f, indent=4)
