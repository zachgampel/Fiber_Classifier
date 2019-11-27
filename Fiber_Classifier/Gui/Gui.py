import tkinter
from tkinter import *
from tkinter import filedialog
from Extractors.Roughness_Extractor import getRoughnessValue
import cv2


def getImage(frame, directory_index):
    f = filedialog.askopenfilename(
        parent=root, initialdir='Desktop\Design II\Fiber_Classifier\Final Images\Wool\Corriedale (Undyed)\Corriedale (Undyed) 0 i=3, j= 3',
        title='Choose file',
        filetypes=[('png images', '.png', '.jpg'), ('gif images', '.gif', '.jpg')]
        )

    directories[directory_index] = f
    
    image = tkinter.PhotoImage(file=f)
    f4 = tkinter.Label(frame, image=image)
    f4.image = image
    f4.pack()


def createMask():
    if directories[0] is not 0:
        print("Image is there")
        label = Label(frame6, text="Calculating mask...").pack()
        roughness, roughness_image, mask = getRoughnessValue(cv2.imread(directories[0]))
        image = tkinter.PhotoImage(file=roughness_image)
        frame6.image = image
        frame6.pack()


# first entry is for input image, second entry is for mask
directories = [0, 0]

root = tkinter.Tk()
root.title("TexID Fiber Classifier")
root.resizable(width="true", height="true")
root.minsize(width=300, height=300)
root.maxsize(width=2000, height=2000)


frame1 = tkinter.Frame(root, borderwidth=2, relief='ridge')
frame2 = tkinter.Frame(root, borderwidth=2, relief='ridge')
frame3 = tkinter.Frame(root, borderwidth=2, relief='ridge')
frame4 = tkinter.Frame(root, borderwidth=2, relief='ridge')
frame5 = tkinter.Frame(root, borderwidth=2, relief='ridge')
frame6 = tkinter.Frame(root, borderwidth=2, relief='ridge')

frame1.grid(column=0, row=0, sticky="nsew")
frame2.grid(column=1, row=0, sticky="nsew")
frame3.grid(column=2, row=0, sticky="nsew")
frame4.grid(column=0, row=1, sticky="nsew")
frame5.grid(column=1, row=1, sticky="nsew")
frame6.grid(column=2, row=1, sticky="nsew")


base_image_button = tkinter.Button(frame1, text="Input fiber image", command = lambda: getImage(frame4, 0))
mask_image_button = tkinter.Button(frame2, text="Input masked image", command = lambda: getImage(frame5, 1))
create_mask_image_button = tkinter.Button(frame3, text="Generate a mask", command = lambda: createMask())

base_image_button.pack(fill="x")
mask_image_button.pack(fill="x")
create_mask_image_button.pack(fill="x")


root.mainloop()
