import filecmp
import os
from glob import glob
for fn in glob('*.jpg'):
    if(filecmp.cmp('frame0.jpg',fn)):
        os.remove(fn)

