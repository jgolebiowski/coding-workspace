#!/usr/bin/python

import sys
import numpy as np
import math

# Script for replicating a unit cell with absolute coordinates to create a supercell

filename = str(sys.argv[1])  # First argument is .cell file
ascale   = int(sys.argv[2])  # Second argument is no times to replicate in a dimension
bscale   = int(sys.argv[3])  # Third argument is no times to replicate in b dimension
cscale   = int(sys.argv[4])  # Fourth argument is no times to replicate in c dimension
pos_digit = 16               # Number of decimal places in atom posns

# Open files and get indicies of important lines
f = open(filename,'r')                         # Open cell file 
cell  = f.readlines()                          # Read file as a list of lines
f.seek(0,0)
for num, line in enumerate(f):                 # Find start and end of atom positions section
    if '%BLOCK POSITIONS_ABS' in line:
        l_1 = num
f.seek(0,0)
for num, line in enumerate(f):
    if '%ENDBLOCK POSITIONS_ABS' in line:
        l_2 = num
f.seek(0,0) 
n = l_2 - l_1                                   # number of atoms 
string = "{0:." + str(pos_digit) + "f}"
for num, line in enumerate(f):                  # Find the start of the lattice vectors (assumed to be BEFORE atom positions)
    if '%BLOCK LATTICE_CART' in line:           # and thus print the new lattice vectors
        l_lat = num
clength = len(cell)                             # Number of lines in the .cell file
f.close()

# Lattice vectors in form:    avec = [ax,ay,az]  
avec = [float(cell[l_lat+1].split()[0]),float(cell[l_lat+1].split()[1]),float(cell[l_lat+1].split()[2])]
bvec = [float(cell[l_lat+2].split()[0]),float(cell[l_lat+2].split()[1]),float(cell[l_lat+2].split()[2])]
cvec = [float(cell[l_lat+3].split()[0]),float(cell[l_lat+3].split()[1]),float(cell[l_lat+3].split()[2])]
newavec = np.dot(ascale,avec)                   # Scale lattice vectors
newbvec = np.dot(bscale,bvec)
newcvec = np.dot(cscale,cvec) 

# Write new lattice vectors
pre_atoms = cell[0:l_1+1]                       # The section of the .cell file before atom positions
pre_atoms[l_lat+1] = str(string.format(newavec[0])) + '\t' + str(string.format(newavec[1])) + '\t' + str(string.format(newavec[2])) + '\n'
pre_atoms[l_lat+2] = str(string.format(newbvec[0])) + '\t' + str(string.format(newbvec[1])) + '\t' + str(string.format(newbvec[2])) + '\n'
pre_atoms[l_lat+3] = str(string.format(newcvec[0])) + '\t' + str(string.format(newcvec[1])) + '\t' + str(string.format(newcvec[2])) + '\n'

# Cycle through each old atom and assign new coordinates
atoms = []
for i in range(1,n):
    for ia in range(0,ascale):
        for ib in range(0,bscale):
            for ic in range(0,cscale):
                atom  = str(cell[l_1 + i].split()[0])
                pos_x = float(cell[l_1 + i].split()[1])                 # Old absolute positions
                pos_y = float(cell[l_1 + i].split()[2])
                pos_z = float(cell[l_1 + i].split()[3])
                absvec = np.array([pos_x,pos_y,pos_z])                  # Vector of old absolute positions
                newabsvec = absvec + np.dot(ia,avec) + np.dot(ib,bvec) + np.dot(ic,cvec)
                newpos_x = float(newabsvec[0])                       # New absolute positions
                newpos_y = float(newabsvec[1])
                newpos_z = float(newabsvec[2])
                atoms.append(atom + '\t' + str(string.format(newpos_x)) + '\t' + str(string.format(newpos_y)) + '\t' + str(string.format(newpos_z)) + '\n')

# Copy the post atom positions portion of the .cell file
post_atoms=cell[l_2:clength]                    # Copy all of the .cell file after the atom positions

# Rewrite .cell file with new atom positions
cell_new = pre_atoms + atoms + post_atoms       # Stich the various parts together to form the full new .cell file
g = open(filename,'w')
g.writelines( cell_new )
g.close

print filename + " updated with a " + str(ascale) + " " + str(bscale) + " " + str(cscale) + " supercell."
