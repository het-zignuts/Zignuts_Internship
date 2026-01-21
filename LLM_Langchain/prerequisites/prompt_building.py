import os

with open("prompt_template.txt", "r") as file:
    prompt_template=file.read()

prompt=prompt_template.format(topic="muffins")

print("Final prompt: \n", prompt)