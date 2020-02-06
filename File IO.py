import os
print(os.listdir())
print(os.getcwd())

with open('/home/rohan/FacialRecognition/helloworld', 'a') as file:
    for i in range(10):
        file.write('HelloPython')
    file.close()