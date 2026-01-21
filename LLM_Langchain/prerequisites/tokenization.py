import tiktoken

enc=tiktoken.get_encoding("cl100k_base")

with open("test_file2.txt", "r") as file:
    text=file.read()

tokens=enc.encode(text)
decoded = enc.decode(tokens)
print("Tokens: \n", tokens)
print(decoded)
print("\n Total no. of tokens: ", len(tokens))