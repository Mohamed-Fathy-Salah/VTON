"""
pipe obj files with tex coordinates to extract the tex coord in npy file with same name
run as `ls *.obj | python extract_tex_coord.py`
"""
import os
from sys import stdin
import numpy as np

if __name__ == '__main__':
    files = stdin.readlines()

    for file in files:
        filename = os.path.splitext(file)[0] 

        with open(file[:-1], "r") as f:
            lines = f.readlines()

        vt = []
        ft = []

        for line in lines:
            line = line.split(' ')
            if line[0] == 'vt' :
                vt.append(line)
            elif line[0] == 'f' :
                ft.append(line)

        with open(f"{filename}_vt.npy", "wb") as f:
            np.save(f, np.array(vt))

        with open(f"{filename}_ft.npy", "wb") as f:
            np.save(f, np.array(ft))
# arr = np.load("./skirt_female.npy")

# with open("blah.txt", "wb") as f:
    # string = str(arr.tolist())
    # f.write(string.encode("ascii"))
