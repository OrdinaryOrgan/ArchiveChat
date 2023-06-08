import json
import os

def load_from_file(file):
    with open(file, 'r') as f:
        return json.load(f)
    
def save_to_file(file, obj):
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    with open(file, 'w+') as f:
        json.dump(obj, f)

def load_from_string(string : str):
    return json.loads(string)

def save_to_string(obj):
    return json.dumps(obj)