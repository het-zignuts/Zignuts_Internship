import json
from json import JSONDecodeError

try:
    with open("manual_json.py", "r") as file:
        try:
            json_data=json.load(file)
            print(json_data)
        except JSONDecodeError as e:
            print("Invalid JSON...")
    with open("manual_json_invalid.py", "r") as file:
        try:
            json_data=json.load(file)
            print(json_data)
        except JSONDecodeError as e:
            print("Invalid JSON...")
except FileNotFoundError as e:
    print("File not found....")