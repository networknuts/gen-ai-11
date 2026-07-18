myfile = open("data.txt","r")

for line in myfile.readlines():
    print(line.strip())

myfile.close()