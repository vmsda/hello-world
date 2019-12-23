#!/usr/bin/env python3

""" 
I am indebted to JAVIDX9 via his video at https://youtu.be/Y37-gB83HKE.
JAVIDX9's clear explanation gave me the courage to tackle the problem.
The implemention of the recursive backtracker algorithm was my sole
responsibility, and any mistakes that may be spotted should not be
attributed to anyone else.
This was my first adventure into the Python/Tkinter world, and it shows!
If you are a beginner, as I still am, perhaps you would profit from
viewing JAVIDX9's video before looking into my clumsy efforts.
"""

import tkinter as tk
import random
from copy import deepcopy

root = tk.Tk()
size = input("Choose the labyrinth side size ex ..10..18..24.. etc: ")
size = int(size)
hunter = None
hunter_cell = 2
prey = None
prey_cell = int(size**2-2)
dir_per_cell = {}

def create_grid(event=None):
    global hunter
    global prey
    print("Draw the rectangles (cells)")
    geo = {}                    # dict of row, col for each rectange
    centres = {}                # dict of centre coords for each rectangle
    d = 20                      # size of side
    x0 = 20                     # starting x position
    x1 = x0 + d
    y0 = 20                     # starting y position
    y1 = y0 + d
    for i in list(range(size)):
        for j in list(range(size)):
            row = i
            col = j
            id = cv.create_rectangle(x0, y0, x1, y1,
                                     fill="white", outline="blue")
            geo[id] = (row, col)
            centres[id] = (x0 + d/2, y0 + d/2)
            x0 = x1
            x1 += d
        x0 = d
        x1 = x0 + d
        y0 = y1
        y1 = y0 + d
        
    # Now, create the neighbors
    print("Now, create the neighbours for each cell")
    next = {}                       # dict of id neighbours for each id
    geo_k = list(geo.keys())        # this line and next allow to get ...
    geo_v = list(geo.values())      # a key from its value
    counter = 0
    for k in geo:
        id = geo[k]
        poss_n = [(id[0],id[1]-1),(id[0],id[1]+1),   # possible neighbours
                  (id[0]-1,id[1]),(id[0]+1,id[1])]   # ... for each id
        next_ids = []
        for each in poss_n[:]:
            if each not in geo_v:
                counter += 1
                poss_n.remove(each)
            else:
                pos = geo_v.index(each)
                n_id = geo_k[pos]
                next_ids.append(n_id)
        next[k] = next_ids
    
    # Draw the lines between cells' centres
    print("Randomly draw all possible connections from each cell, " +
          "remove neighboring connected cell from 'next'")
    next_new = deepcopy(next)
    stack = []
    visited = []
    lines_cells = {} 
    cell = 1
    visited.append(cell)
    stack.append(cell)
    while len(visited) < size**2:
        if next_new[cell] != []:
            n = random.choice(next_new[cell])
            if n not in visited:
                id_line = cv.create_line(centres[cell], centres[n])
                lines_cells[id_line] = [cell, n]
                visited.append(n)
                stack.append(n)
                next_new[cell].remove(n)
                next_new[n].remove(cell)
                cell = n
            elif len(stack) > 0:
                cell = stack.pop()  # pop to find neighbor not yet visited
            else: break
        elif len(stack) > 0:
            cell = stack.pop()  # if previous cell had no unvisited neighbours
        else: break
    
    # Eliminate duplicates in remainder of "next"
    print("Eliminate one of the two instances of each nonconnection")
    next_uni = deepcopy(next_new)
    nonconn_all = []          # dict turning it into a nested list
    for k in next_uni:          # fill nonconn_all          
        v = next_uni[k]
        for i in range(len(v)):
            nonconn_all.append([k, v[i]])
    nonconn_unique = []       
    for item in nonconn_all:      
        if sorted(item) not in nonconn_unique:   #eliminate reverse nonconn...
            nonconn_unique.append(sorted(item))     # between the same 2 cells    

    #Build the walls
    print("Now we are ready to draw the walls between each cell pair")
    walls = []
    for item in nonconn_unique:
        cellB = cv.coords(item[1])
        cellA = cv.coords(item[0])
        wall_id = cv.create_line(cellB[0], cellB[1], cellA[2], cellA[3],
                                 tags="WALL", width=3, fill="green")
        walls.append(wall_id)
    maze_outline = cv.create_line(d, d, d*(size+1), d, d*(size+1), d*(size+1),
                                  d, d*(size+1), d, d, tags="WALL", width=4,
                                  joinstyle="round", fill="green")
    
    for item in geo:
        cv.itemconfigure(item, outline="white")
    for item in lines_cells.keys():
        cv.itemconfigure(item, fill="white")
   
    hunter = cv.create_oval(cv.coords(2)[0]+4, cv.coords(2)[1]+4,
                            cv.coords(2)[2]-4,cv.coords(2)[3]-4, fill="blue")
    prey = cv.create_oval(cv.coords(size**2-2)[0]+4, cv.coords(size**2-2)[1]+4,
                          cv.coords(size**2-2)[2]-4, cv.coords(size**2-2)[3]-4,
                          fill="yellow")

    #Build directions per cell: up, down, left, right
    values_lines_cells = list(lines_cells.values())
    global dir_per_cell
    for v in values_lines_cells:
        A = v[0]
        B = v[1]
        dirA = []
        dirB = []
        if A - B == -size:
            dirA.append("Down")
            dirB.append("Up")
        elif A - B == size:
            dirA.append("Up")
            dirB.append("Down")
        elif A - B == -1:
            dirA.append("Right")
            dirB.append("Left")
        elif A - B == 1:
            dirA.append("Left")
            dirB.append("Right")
        dir_per_cell[A] = dir_per_cell.get(A,[]) + dirA
        dir_per_cell[B] = dir_per_cell.get(B,[]) + dirB
    
def hunter_move(event):
    global prey_cell
    global hunter
    global hunter_cell
    global dir_per_cell
    try:
        if event.keysym in dir_per_cell[hunter_cell]:  
            if event.keysym == "Up":
                xAmount = 0
                yAmount = -20
                hunter_cell = hunter_cell - size
            elif event.keysym == "Down":
                xAmount = 0
                yAmount = 20
                hunter_cell = hunter_cell + size
            elif event.keysym == "Left":
                xAmount = -20
                yAmount = 0
                hunter_cell = hunter_cell - 1
            elif event.keysym == "Right":
                xAmount = 20
                yAmount = 0
                hunter_cell = hunter_cell + 1            
        else:
            pass
        cv.move(hunter, xAmount, yAmount)
        if hunter_cell == prey_cell:
            root.destroy()

    except UnboundLocalError:
        print("Press Up or Down or Left or Right")
        
cv = tk.Canvas(root, bd=5, highlightthickness=0, relief="groove",
               width=size*20 + 40, height=size*20 + 40)
cv.pack(fill="both", expand=1)
cv.bind('<Configure>', create_grid())
cv.bind('<Any-KeyPress>', hunter_move)
cv.focus_set()
cv.tag_bind(hunter, '<Any-KeyPress>, hunter_move')
cv.focus(hunter)
root.mainloop()
