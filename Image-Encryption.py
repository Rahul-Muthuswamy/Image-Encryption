import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mbox
from PIL import ImageTk, Image
import cv2
import numpy as np
window = tk.Tk()
window.geometry("1000x700")
window.title("Image Encryption Decryption")
window.configure(bg="#1A1A2E")
global count, eimg
panelB = None
panelA = None
def getpath(path):
    return '/'.join(path.split(r'/')[:-1])
def getfilename(path):
    return path.split(r'/')[-1].split('.')[0]
def openfilename():
    return filedialog.askopenfilename(title='Open')
def open_img():
    global x, panelA, panelB, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    eimg = img
    img = ImageTk.PhotoImage(img)
    location = getpath(x)
    filename = getfilename(x)
    if panelA is None or panelB is None:
        panelA = tk.Label(image=img, bg="#1A1A2E", bd=2, relief="solid")
        panelA.image = img
        panelA.place(x=50, y=180, width=400, height=400)
        panelB = tk.Label(image=img, bg="#1A1A2E", bd=2, relief="solid")
        panelB.image = img
        panelB.place(x=550, y=180, width=400, height=400)
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img
def en_fun():
    global x, image_encrypted, key
    image_input = cv2.imread(x, 0)
    (x1, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0
    mu, sigma = 0, 0.1  # Mean and standard deviation
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    image_encrypted = image_input / key
    cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
    imge = Image.open('image_encrypted.jpg')
    imge = ImageTk.PhotoImage(imge)
    panelB.configure(image=imge)
    panelB.image = imge
    mbox.showinfo("Encrypt Status", "Image Encrypted Successfully.")
def de_fun():
    global image_encrypted, key
    image_output = image_encrypted * key
    image_output *= 255.0
    cv2.imwrite('image_output.jpg', image_output)
    imgd = Image.open('image_output.jpg')
    imgd = ImageTk.PhotoImage(imgd)
    panelB.configure(image=imgd)
    panelB.image = imgd
    mbox.showinfo("Decrypt Status", "Image Decrypted Successfully.")
def reset():
    global x, eimg
    image = cv2.imread(x)[:, :, ::-1]
    eimg = Image.fromarray(image)
    image = ImageTk.PhotoImage(eimg)
    panelB.configure(image=image)
    panelB.image = image
    mbox.showinfo("Success", "Image Reset to Original Format!")
def save_img():
    global eimg
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    eimg.save(filename)
    mbox.showinfo("Success", "Encrypted Image Saved Successfully!")
header_frame = tk.Frame(window, bg="#16213E", pady=20)
header_frame.pack(fill="x")
header_label = tk.Label(header_frame, text="Image Encryption & Decryption", font=("Verdana", 28, "bold"), fg="#E94560", bg="#16213E")
header_label.pack()
img_frame = tk.Frame(window, bg="#1A1A2E")
img_frame.pack(pady=20)
btn_frame = tk.Frame(window, bg="#1A1A2E")
btn_frame.pack(pady=10)
choose_btn = tk.Button(btn_frame, text="Choose Image", command=open_img, font=("Verdana", 16), bg="#0F3460", fg="#FFFFFF", padx=20, pady=10, relief="flat")
choose_btn.grid(row=0, column=0, padx=10)
save_btn = tk.Button(btn_frame, text="Save Image", command=save_img, font=("Verdana", 16), bg="#0F3460", fg="#FFFFFF", padx=20, pady=10, relief="flat")
save_btn.grid(row=0, column=1, padx=10)
encrypt_btn = tk.Button(btn_frame, text="Encrypt", command=en_fun, font=("Verdana", 16), bg="#533483", fg="#FFFFFF", padx=20, pady=10, relief="flat")
encrypt_btn.grid(row=1, column=0, padx=10, pady=10)
decrypt_btn = tk.Button(btn_frame, text="Decrypt", command=de_fun, font=("Verdana", 16), bg="#533483", fg="#FFFFFF", padx=20, pady=10, relief="flat")
decrypt_btn.grid(row=1, column=1, padx=10, pady=10)
reset_btn = tk.Button(btn_frame, text="Reset", command=reset, font=("Verdana", 16), bg="#E94560", fg="#FFFFFF", padx=20, pady=10, relief="flat")
reset_btn.grid(row=2, column=0, columnspan=2, pady=10)
def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()
exit_btn = tk.Button(window, text="EXIT", command=exit_win, font=("Verdana", 16, "bold"), bg="#F3722C", fg="#FFFFFF", padx=20, pady=10, relief="flat")
exit_btn.pack(pady=20)
window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
