import os
    
prof_data={}

with open("test_file2.txt", "r") as file:
    line= file.readline()
    while line:
        tkns=line.strip().split(":")
        key=tkns[0].strip()
        value=tkns[1].strip()
        prof_data[key]=value
        line=file.readline()

print(prof_data)
print(type(prof_data))