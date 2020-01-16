#!/usr/bin/env python
# coding: utf-8

# In[5]:


from PIL import Image, ImageChops
from math import inf as infinity
import numpy as np


# In[9]:


# Black
COLOR_WALL = (0, 0, 0)
# White
COLOR_PATH = (255, 255, 255)

# Red
COLOR_START = (255, 0, 0)
# Green
COLOR_END = (0, 255, 0)
# Blue
COLOR_SOLVED = (0, 0, 255)
COLOR_VISITED = (128,128,128)

#parser = argparse.ArgumentParser(description="Solve input PNG maze file")
#parser.add_argument("-i", "--input", help="Maze file. Defaults to maze.png",
#                    default="maze.png", required=False)
#parser.add_argument("-o", "--output", default="solved.png",
#                    help="PNG file to output to. Defaults to solved.png")

#args = parser.parse_args()
def load_img(image_path, remove_border, start_loc = 'top'):
    output=image_path+'marked.png'
    try:
        image = Image.open(image_path).convert('RGB')
        pixels = image.load()
    except:
        print("Could not load file", image)
        exit()
    #print(pixels[1,1])
    if remove_border==True:
        image=trim(image)
        pixels = image.load()
    width, height = image.size
    
    if start_loc=='top':
        for i in range(width):
            if pixels[i,0] == COLOR_PATH:
                pixels[i,0]=COLOR_END
            if pixels[i,height-1] == COLOR_PATH:
                pixels[i,height-1]=COLOR_START
        image.save(output, "PNG") 
        
    elif start_loc=='left':
        for i in range(height):

            if pixels[0,i] == COLOR_PATH:
                pixels[0,i]=COLOR_END
            if pixels[width-1,i] == COLOR_PATH:
                pixels[width-1,i]=COLOR_START
        image.save(output, "PNG")   
    return width,height,width*height

# In[10]:


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
