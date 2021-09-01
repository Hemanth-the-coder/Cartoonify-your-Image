import cv2   #used for reading images and processing them 
import easygui  #to use filebox while uploading 
import numpy as np #dealing with matrix of 1 and 0
import imageio    #provides interface for imreading and imwriting 
import sys     
import matplotlib.pyplot as plt    #for visualising and ploting
import os       # to interact with directories for saving the images
import tkinter as tk    #to implement the basic gui 
from tkinter import filedialog
from tkinter import *  
from PIL import ImageTk , Image    #deal with images other than png 
root=Tk()
root.configure(background='gray')
root.geometry('400x400')
def upload():
    imagepath=easygui.fileopenbox()
    cartoon(imagepath)
uploadimage=Button(text="upload and cartoonify your image",fg="white", bg="black",width=30, command=upload ,padx=5).pack(pady=10)
def save(cartoonedimg,imagepath):
    directory=os.path.dirname(imagepath)
    extension=os.path.splitext(imagepath)[1]
    path1=os.path.join(directory, 'cartoonedimage'+extension)
    print(path1)
    cv2.imwrite(path1, cv2.cvtColor(cartoonedimg, cv2.COLOR_BGR2RGB))
def cartoon(imagepath):
    originalimage=cv2.imread(imagepath)
    # print(originalimage)  #as image is stored as numbers , it will print numbers 
    originalimage=cv2.cvtColor(originalimage,cv2.COLOR_BGR2RGB)   #making image colorful
    # print(originalimage)
    # plt.imshow(originalimage)
    # plt.show()
    originalimage=cv2.resize(originalimage,(960,540))
    # plt.imshow(originalimage)
    # plt.show()
    grayscaleimage=cv2.cvtColor(originalimage,cv2.COLOR_BGR2GRAY)   #making it to gray
    # resize=cv2.resize(grayscaleimage,(960,540))
    # plt.imshow(resize)
    # plt.show()
    smoothened=cv2.medianBlur(grayscaleimage,5)   # to smoothening image edges are not preserved
    # plt.imshow(smoothened)
    # plt.show()
# Simple threshold function pseudo code
# if src(x,y) > thresh
#   dst(x,y) = maxValue
# else
#   dst(x,y) = 0  if the value of particular pixel is greater than threshold it will set to 255 , 
#  which is white , and if it is less than the threshold it will set to 0 , by this we get edges 
    getedge=cv2.adaptiveThreshold(smoothened,10,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)  #retriving the edges
    plt.imshow(getedge, cmap='gray')
    plt.show()
    colorimage=cv2.bilateralFilter(originalimage,9,255,255)   #cleaning the image with preserving edges
    # plt.imshow(colorimage)
    # plt.show()
    cartooned=cv2.bitwise_and(colorimage,colorimage,mask=getedge)   #masking the edges the the colorimage 
    cartooned=cv2.resize(cartooned, (300,300))
    plt.imshow(cartooned , cmap='gray')
    saved=Button(text="save",fg="white", bg="black",width=30, command=lambda :save(cartooned,imagepath) ,padx=5).pack(pady=20)
    plt.show()
root.mainloop()