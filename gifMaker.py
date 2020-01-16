#!/usr/bin/env python
# coding: utf-8

# In[3]:


import imageio
import glob
import os


# In[8]:


def make_searched_gif():
    if os.path.exists("searched_movie.gif"):
        os.remove("searched_movie.gif")
    file_list=[os.path.basename(x) for x in glob.glob('test/*')]
    file_list.sort(key=lambda fname: int(fname.split('.')[0]))
    if len(file_list)>5000:
        frame_speed = 100
    elif len(file_list)<5000:
        frame_speed = 50
    with imageio.get_writer('searched_movie.gif', mode='I',fps=30) as writer:
        for count,filename in enumerate(file_list,1):
            if count% frame_speed == 0:
                image = imageio.imread('test'+'/'+filename)
                writer.append_data(image)

def make_solved_gif():
    if os.path.exists("solved_movie.gif"):
        os.remove("solved_movie.gif")    
    file_list=[os.path.basename(x) for x in glob.glob('solved/*')]
    file_list.sort(key=lambda fname: int(fname.split('.')[0]))
    if len(file_list)>500:
        frame_speed = 5
    elif len(file_list)<500:
        frame_speed = 2
    with imageio.get_writer('solved_movie.gif', mode='I',fps=30) as writer:
        for count,filename in enumerate(file_list,1):
            if count% frame_speed == 0:
                image = imageio.imread('solved'+'/'+filename)
                writer.append_data(image)


# In[9]:





# In[ ]:




