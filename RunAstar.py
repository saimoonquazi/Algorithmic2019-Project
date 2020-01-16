#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/python3

from PIL import Image
from math import inf as infinity
import argparse
import numpy as np
import imageio
import dijkstra as d
from math import inf as infinity

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

class Graph:
    def __init__(self, graph, initial, destination):
        self.graph = graph
        self.initial_node = graph[initial[1]][initial[0]]
        self.destination_node = graph[destination[1]][destination[0]]

    def __str__(self):
        return "\n".join([" ".join([str(column).ljust(6) for column in row])
                          for row in self.graph])

    def get_nodes(self):
        return [node for row in self.graph for node in row]

    def get_neighbors(self, node):
        neighbors = []
        if (node.y != 0):
            neighbors.append(self.graph[node.y - 1][node.x])
        if (node.y != len(self.graph) - 1):
            neighbors.append(self.graph[node.y + 1][node.x])
        if (node.x != 0):
            neighbors.append(self.graph[node.y][node.x - 1])
        if (node.x != len(self.graph[node.y]) - 1):
            neighbors.append(self.graph[node.y][node.x + 1])
        return neighbors
        


class Node:
    tentative_distance = None
    fScore=None
    heuristic_distance=None
    visited = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.tentative_distance)

    def distance_to(self, other):
        return 1
    
def astar(graph,pixels,image):
    initial_node = graph.initial_node
    destination_node = graph.destination_node
    i=0
        # Mark all nodes unvisited. Create a set of all the unvisited nodes called
        # the unvisited set.
    unvisited = set(graph.get_nodes())

        # Assign to every node a tentative distance value: set it to zero for our
        # initial node and to infinity for all other nodes.
    initial_node.tentative_distance = 0
    initial_node.heuristic_distance=abs((destination_node.x-initial_node.x) + (destination_node.y-initial_node.y))
    #print(initial_node.heuristic_distance)
    initial_node.fScore=initial_node.heuristic_distance
    
    
    for node in unvisited:
        if node and node is not initial_node:
            node.tentative_distance = infinity
            node.fScore=infinity

    current_node = initial_node

    while not destination_node.visited:
            # For the current node, consider all of its unvisited neighbors and
            # calculate their tentative distances through the current node. Compare
            # the newly calculated tentative distance to the current assigned value
            # and assign the smaller one.
        for neighbor in graph.get_neighbors(current_node):
            if not neighbor or neighbor.visited:
                continue
            new_tentative_distance = current_node.tentative_distance + current_node.distance_to(neighbor)
            if neighbor.tentative_distance > new_tentative_distance:
                
                neighbor.tentative_distance = new_tentative_distance
                neighbor.heuristic_distance=abs((destination_node.x-neighbor.x) + (destination_node.y-neighbor.y))
                neighbor.fScore=neighbor.tentative_distance+neighbor.heuristic_distance
                

            # When we are done considering all of the neighbors of the current node
            # mark the current node as visited and remove it from the unvisited set
            # A visited node will never be checked again.
        current_node.visited = True
        unvisited.remove(current_node)

            # Move to the next unvisited node with the smallest tentative distance
        smallest_tentative_distance = infinity
        smallest_fScore = infinity
        
        for node in unvisited:
            #if node:
                #print(node.fScore)
            if node and node.fScore<smallest_fScore and node.tentative_distance < smallest_tentative_distance:
                #print(node.fScore)
                pixels[node.x, node.y] = COLOR_VISITED
                image.save('test/'+str(i), "PNG")
                smallest_tentative_distance = node.tentative_distance
                smallest_fScore=node.fScore
                current_node = node
                i=i+1

    return destination_node.tentative_distance,destination_node.fScore,i  

def runAstar(img_file):
    
    image=img_file
    output='maze1_solved'
    try:
        image = Image.open(image)
        pixels = image.load()
    except:
        print("Could not load file", image)
        exit()

    height, width=image.size
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
    graph = Graph(nodes, initial_coords, destination_coords)

    destination_distance,destination_fScore,nodes_checked = astar(graph,pixels,image)

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
    smallest_fScore=destination_fScore
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
                if neighbor is not None:
                    pixels[neighbor.x, neighbor.y] = COLOR_VISITED
        pixels[current_node.x, current_node.y] = COLOR_SOLVED
        #image.save('test/'+output+str(i), "PNG")
        #i=i+1
        #out_images.append(image)
        path_x.append(current_node.x)
        path_y.append(current_node.y)    
        
    gif_image = Image.open(img_file)
    gif_pixels = gif_image.load()
    for i in range(len(path_x)):
        gif_pixels[path_x[i], path_y[i]] = COLOR_SOLVED
        gif_image.save('solved/'+str(i), "PNG")
    #image.save(output, "PNG")
    return len(path_x),nodes_checked