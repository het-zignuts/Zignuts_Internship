import os
import json

with open("test_file.json", "r") as file:
    personal_info=json.load(file)

print(personal_info)
print(type(personal_info))

personal_info["Age"] = 21

with open("test_file.json", "w") as file:
    json.dump(personal_info, file)

with open("test_file.json", "r") as file:
    personal_info=json.load(file)

print(personal_info)
print(type(personal_info))

