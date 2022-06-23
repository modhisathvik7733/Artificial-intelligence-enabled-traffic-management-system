import os
from PIL import Image

list = os.listdir('tripleride') # dir is your directory path
number_files = len(list)
print(number_files)
img_dir = r"tripleride"
c=0
while(c!=number_files):
    c+=1
    for filename in os.listdir(img_dir):
        filepath = os.path.join(img_dir, filename)
        try:
            with Image.open(filepath) as im:
                x, y = im.size
        except:
            os.remove(filepath)
