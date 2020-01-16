#!/usr/bin/env python
# coding: utf-8

# In[17]:


#!/usr/bin/python3

from PIL import Image
import dijkstra as d
from math import inf as infinity
import argparse
import numpy as np
import imageio

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

def run_djikstra(image_file):    
    image=image_file
    output=image_file+'maze1_solved'
    try:
        image = Image.open(image)
        pixels = image.load()
    except:
        print("Could not load file", image)
        exit()

    nodes = [[None for _ in range(image.width)] for __ in range(image.height)]
    for x in range(image.width):
        for y in range(image.height):
            pixel = pixels[x, y]
            #print(pixel)
            if pixel == COLOR_WALL:
                nodes[y][x] = None
            else:
                nodes[y][x] = d.Node(x, y)

            if pixel == COLOR_START:
                initial_coords = (x, y)
            if pixel == COLOR_END:
                destination_coords = (x, y)

    graph = d.Graph(nodes, initial_coords, destination_coords)

    destination_distance,nodes_checked = d.dijkstra(graph,image,pixels,COLOR_VISITED)

    initial_node = graph.graph[initial_coords[1]][initial_coords[0]]
    destination_node = graph.graph[destination_coords[1]][destination_coords[0]]
    nodes = graph.get_nodes()

    for node in nodes:
        if node:
            node.visited = False
    path_x=[]
    path_y=[]
    out_images = []
    i=0
    current_node = destination_node
    smallest_tentative_distance = destination_distance
    # Go from destination node to initial node to find path
    while current_node is not initial_node:
        neighbors = graph.get_neighbors(current_node)
        for neighbor in neighbors:
            if not neighbor or neighbor.visited:
                continue
            if neighbor.tentative_distance < smallest_tentative_distance:
                smallest_tentative_distance = neighbor.tentative_distance
                neighbor.visited = True
                current_node = neighbor
                
        pixels[current_node.x, current_node.y] = COLOR_SOLVED
        #image.save('test/'+output+str(i), "PNG")
        #i=i+1
        #out_images.append(image)
        path_x.append(current_node.x)
        path_y.append(current_node.y) 
    
    gif_image = Image.open(image_file)
    gif_pixels = gif_image.load()
    for i in range(len(path_x)):
        gif_pixels[path_x[i], path_y[i]] = COLOR_SOLVED
        gif_image.save('solved/'+str(i), "PNG")
    #imageio.mimsave('solution.gif', out_images)
    #image.save(output, "PNG")
    return len(path_x),nodes_checked

