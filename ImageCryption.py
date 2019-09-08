# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 23:25:42 2019

@author: 夏日有凉风
"""
import numpy as np
import time
from tkinter import *
from PIL import ImageTk
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import PIL.Image
import os



def print_no_pwd_msg():
	tkinter.messagebox.showinfo("Encryption key required", "Please enter encryption key before selecting a file.")

def open_image():
	# check whether a password has been entered
	if ( passwd.get() ):
		# open window to choose the desired file
		filename = filedialog.askopenfilename()

		# extract the file name and its extension
		infile, file_extension = os.path.splitext(filename)
		print(infile,file_extension)
		encryption(filename)
	else:
		print_no_pwd_msg()

def open_image2():
	# check whether a password has been entered
	if ( passwd.get() ):

		# open window to choose the desired file
		filename = filedialog.askopenfilename()

		# extract the file name and its extension
		infile, file_extension = os.path.splitext(filename)
		print(infile,file_extension)
		decryption(filename)
	else:
		print_no_pwd_msg()
'''
加密:
	-key: 密钥
	-imgpath: 待加密图像路径
	-start: 将生成的混沌序列，从第start个之后开始作为加密用序列
'''
def encryption( imgpath, key=3.78,start=500, x0=0.1):
	if key > 4 or key < 3.57:
		print('[Error]: Key must between <3.57-4>...')
		return None
	if x0 >= 1 or x0 <= 0:
		print('[Error]: x0 must between <0-1>...')
		return None
	img = PIL.Image.open(imgpath)
	img_en = PIL.Image.new(mode=img.mode, size=img.size)
	width, height = img.size
	chaos_seq = np.zeros(width * height)
	for _ in range(start):
		x = key * x0 * (1 - x0)
		x0 = x
	for i in range(width * height):
		x = key * x0 * (1 - x0)
		x0 = x
		chaos_seq[i] = x
	idxs_en = np.argsort(chaos_seq)
	i, j = 0, 0
	for idx in idxs_en:
		col = int(idx % width)
		row = int(idx // width)
		img_en.putpixel((i, j), img.getpixel((col, row)))
		i += 1
		if i >= width:
			j += 1
			i = 0
	img_en.save('encryption.%s' % imgpath.split('.')[-1], quality=100)
	tkinter.messagebox.showinfo("Susseful!","The encryption image has saved!")

'''
解密:
	-key: 密钥
	-imgpath: 待解密图像路径
	-start: 将生成的混沌序列，从第start个之后开始作为解密用序列
'''
def decryption(imgpath,key=3.78, start=500, x0=0.1):
	if key > 4 or key < 3.57:
		print('[Error]: Key must between <3.57-4>...')
		return None
	if x0 >= 1 or x0 <= 0:
		print('[Error]: x0 must between <0-1>...')
		return None
	img =  PIL.Image.open(imgpath)
	img_de = PIL.Image.new(img.mode, img.size)
	width, height = img.size
	chaos_seq = np.zeros(width * height)
	for _ in range(start):
		x = key * x0 * (1 - x0)
		x0 = x
	for i in range(width * height):
		x = key * x0 * (1 - x0)
		x0 = x
		chaos_seq[i] = x
	idxs_de = np.argsort(chaos_seq)
	i, j = 0, 0
	for idx in idxs_de:
		col = int(idx % width)
		row = int(idx // width)
		img_de.putpixel((col, row), img.getpixel((i, j)))
		i += 1
		if i >= width:
			j += 1
			i = 0
	img_de.save('decryption.%s' % imgpath.split('.')[-1], quality=100)
	tkinter.messagebox.showinfo("Susseful!","解密后图像已保存")

# initialize the GUI
root = Tk()

# set the title of the window
root.title("Just-Try   :   Python Image Encrypter")

# set the size of the window
window = Frame(root, width=720, height=228, background='white')
window.pack_propagate(0)
window.pack()

img = ImageTk.PhotoImage(file='logo1.jpg')
label = Label(window, image=img, borderwidth=0, relief="groove")
label.pack()

passwdLabel = Label(window, text="Enter encryption key (3.57<key<=4) to encrypt/decrypt image:", bg='white')
passwdLabel.pack()

# password input field
passwd = Entry(window, show="*", width=30)
passwd.pack()
print(passwd)

# select image button
selectImg = Button(window, text="选择待加密图片", command=open_image)
selectImg.pack(pady=4)
# select image button /decryption
selectImg = Button(window, text="选择待解密图片", command=open_image2)
selectImg.pack(pady=4)
# quit button
quit = Button(window, text="Quit", command=window.quit)
quit.pack({"side": "bottom"}, pady=10)

# instantiate the application
root.mainloop()
