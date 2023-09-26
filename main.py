# Watermarking App

from tkinter import *
from PIL import ImageTk, Image, ImageFont, ImageDraw
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import matplotlib.pyplot as plt
import numpy as np

logo_path = None
image_path = None


window = Tk()
window.title("Watermarking App")
window.minsize(width=500, height=700)

window.grid_columnconfigure(0, weight=1)

label = Label(text="Make your background and logo selections!")
label.grid(row=0, column=0)

# Global creation value, so we can re-use the program and delete it when a new selection is made
creation = Label(text='PLACEHOLDER')
error = Label(text="")
def watermark(background, logo):
    global creation
    global error
    try:
        background_img = Image.open(image_path)
        logo_img = Image.open(logo_path)

        logo_width, logo_height = logo_img.size
        background_width, background_height = background_img.size

        if logo_width > background_width or logo_height > background_height:
            logo_img = logo_img.resize((background_width, background_height))

        max_width = 500
        pixels_x, pixels_y = tuple([int(max_width / background_img.size[0] * x) for x in background_img.size])

        result_image = Image.new('RGBA', background_img.size)
        result_image.paste(background_img, (0, 0))
        logo_x = 0
        logo_y = 0
        result_image.paste(logo_img, (logo_x, logo_y), mask=logo_img.split()[3])
        photo = ImageTk.PhotoImage(result_image.resize((pixels_x, pixels_y)))
        creation = Label(window, image=photo)
        creation.image = photo
        creation.grid(row=4, column=0)
        return;
    except AttributeError:
        error.destroy()
        print("Please select a valid background and logo")
        error = Label(text="Please select a valid background and logo")
        error.grid(row=4, column=0)


# Selects the background image
def upload_file():
    global image_path
    image_path = filedialog.askopenfilename()

# Selects the logo image, will provide error if unusable watermark or none selected
def upload_watermark():
    global logo_path
    global error
    logo_path = filedialog.askopenfilename()
    try:
        logo_img = Image.open(logo_path)
        print(logo_img.split()[3])
    except IndexError:
        error.destroy()
        print("Incorrect watermark selection!")
        error = Label(text="Incorrect watermark selection!")
        error.grid(row=4, column=0)
        logo_path = None
    except AttributeError:
        error.destroy()
        print("Please make a selection!")
        error = Label(text="Please make a selection!")
        error.grid(row=4, column=0)
        logo_path = None





# If the watermarking program was used, this will clear the previous image
def clear_image():
    global creation
    creation.destroy()
    return;

# Selects a background photo
button1 = Button(text="Select Photo", command=upload_file)
button1.grid(row=1, column=0)

# Selects a logo photo
button2 = Button(text="Select watermark", command=upload_watermark)
button2.grid(row=2, column=0)

# Execute placing your logo on the background
button3 = Button(text="Show watermark", command=lambda: [clear_image(), watermark(image_path, logo_path)])
button3.grid(row=3, column=0)

window.mainloop()
