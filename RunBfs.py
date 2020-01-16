#!/usr/bin/env python
# coding: utf-8

# In[12]:


import sys

from queue import Queue
from PIL import Image
import imageio
import glob
import os

#start = (400,984)
#end = (398,25)

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

def iswhite(value):
    if value == COLOR_PATH:
        return True

def getadjacent(n):
    x,y = n
    return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]


def BFS(start, end, pixels,img_width,img_height,image):
    if not os.path.exists('test'):
        os.makedirs('test')
    if not os.path.exists('solved'):
        os.makedirs('solved')
    adjacent_pixels=[]
    i=0
    queue = Queue()
    #queue=[]
    queue.put([start]) # Wrapping the start tuple in a list
    while not queue.empty():
 
        path = queue.get() 
        pixel = path[-1]
        #print(pixel)
        if pixel == end:
            return path,i
        
        for adjacent in getadjacent(pixel):
            x,y = adjacent
            if x>img_width-1 or y>img_height-1:
                continue
            else:    
                if iswhite(pixels[x,y]) or pixels[x,y]==COLOR_END:
                    pixels[x,y] = COLOR_VISITED  # see note
                    image.save('test/'+str(i), "PNG")
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.put(new_path)
                    i=i+1
    return path, i
    #print("Queue has been exhausted. No answer was found.")




# In[18]:


def run_BFS(img_file):
    image=img_file
    output='maze1_solved'
    try:
        image = Image.open(image)
        pixels = image.load()
    except:
        print("Could not load file", image)
        exit()
    height, width=image.size
    for x in range(image.width):
        for y in range(image.height):
            pixel = pixels[x, y]
            if pixel == COLOR_START:
                initial_coords = (x, y)
            if pixel == COLOR_END:
                destination_coords = (x, y)    
    #print(destination_coords)
    path,nodes_visited = BFS(initial_coords, destination_coords, pixels,width,height,image)
    #print(path)
    path_img = Image.open(img_file)
    #path_img.save('output', "PNG")
    path_pixels = path_img.load()
    m=0
    for position in path:
        x,y = position
        path_pixels[x,y] = COLOR_SOLVED  
        path_img.save('solved/'+str(m), "png")
        m=m+1
    #path_img.save(output, "PNG")
    return len(path),nodes_visited




# In[ ]:




