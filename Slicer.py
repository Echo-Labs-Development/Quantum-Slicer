import tkinter as tk
import math
from tkinter import filedialog, Text, mainloop
from math import floor, sqrt, pow

print("Loading")

size = 1
pArea = [2, 2, 2]
nSize = 0.4

def ArrayAdd(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def ArraySub(a, b):
    return [a[i] - b[i] for i in range(len(a))]

def ArrayMult(a, v):
    return [a[i] * v for i in range(len(a))]

def TriInterpolat(a, b, list):
    if round(ArraySub(b, a)[0]+ArraySub(b, a)[1]+ArraySub(b, a)[2]) > 0:
        qual = sqrt(round(ArraySub(b, a)[0]+ArraySub(b, a)[1]+ArraySub(b, a)[2]))
        for i in range(int(qual)):
            list.append(ArrayAdd(ArrayMult(ArraySub(b, a), (qual/size)*i), a))
def OpenObj():
    objFile = filedialog.askopenfilename(initialdir="/", title="Select Obj", filetypes=(("Wavefront", "*.obj"), ("all files", "*.*")))
    with open(objFile) as baseObj:
        baseGCode = []
        baseGAdd = []
        gCode = []
        for x in range(pArea[0]*int(pow(nSize, -1))):
            for y in range(pArea[1]*int(pow(nSize, -1))):
                for z in range(pArea[2]*int(pow(nSize, -1))):
                    gCode.append(["n",x, y, z])
        for line in baseObj.readlines():
            if line.startswith("v "):
                baseAdd = line.split()
                add = [floor(float(baseAdd[1])*1000)/1000, floor(float(baseAdd[2])*1000)/1000, floor(float(baseAdd[3])*1000)/1000]
                baseGCode.append(add)
            if line.startswith("f "):
                baseAddA = line.split()
                baseFace = []
                for part in baseAddA[1:]:
                    baseFace.append(int(part.split('/')[0]) - 1)
                baseGAdd.append(baseFace)
        max = 0
        min = 0
        for i in baseGCode:
            if abs(i[0]) > max:
                max = abs(i[0])
            if abs(i[1]) > max:
                max = abs(i[1])
            if abs(i[2]) > max:
                max = abs(i[2])
            if i[0] < min:
                min = -i[0]
            if i[1] < min:
                min = -i[1]
            if i[2] < min:
                min = -i[2]
        change = size/max
        for i in baseGCode:
            i[0] *= change
            i[1] *= change
            i[2] *= change
            i[0] += min
            i[1] += min
            i[2] += min

        gAdd = []
        for face in baseGAdd:
            interps = []
            for j in range(len(face)):
                TriInterpolat(baseGCode[face[j-1]], baseGCode[face[j]], interps)
            for l in interps:
                TriInterpolat(baseGCode[face[-1]], l, gAdd)
        for vert in gAdd:
            for i in gCode:
                if [round(vert[0]), round(vert[1]), round(vert[2])] == i:
                    i[0] = "p"
    i = 0
    gCodeFile = open("test.gcode", "r")
    while gCodeFile.read() != "" or i == 0:
        if i == 0:
            gCodeFile = open(objFile.split("/")[len(objFile.split("/"))-1].split(".")[0]+".gcode", "a")
        else:
            print("File has been used")
            gCodeFile = open(objFile.split("/")[len(objFile.split("/"))-1].split(".")[0]+str(i)+".gcode", "a")
        i += 1

def DownloadGCode():
    print("downloaded")

root = tk.Tk()

root.title("Quantum Slicer") 
root.geometry('400x200')

openObj = tk.Button(root, text="Open Obj File", bg="#0000FF", activebackground="#00008B", foreground="white", command=OpenObj)
openObj.pack()

mainloop()
