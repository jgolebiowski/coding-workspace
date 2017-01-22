#!/usr/bin/python

#The code extracts atomic positions from the .geom file from CASTEP
import sys

#open file as first parameter
seedname = str(sys.argv[1]) # First argument is a CASTEP seedname

#read in the file 
f=open(seedname+'.geom','r')
geomlines = f.readlines()
f.close

#reverse the file to find the lst positions 
rev_geomlines=geomlines[::-1]

#extract the lines with abs positions of atoms
block_coords=[]
for line in rev_geomlines:
	if '<-- E' in line:
		break
	if '<-- R' in line:
		block_coords.append(line)
#reverse the coords back 
block_coords=block_coords[::-1]

#extract only the atom species and positions, change the coords to angstroms
coords=[]
changer=0.5291772109217
for atom in block_coords:
	species=atom.split()[0]
	pos_x=float(atom.split()[2])*changer
	pos_y=float(atom.split()[3])*changer
	pos_z=float(atom.split()[4])*changer
	coords.append(species+'\t'+str(pos_x)+'\t'+str(pos_y)+'\t'+str(pos_z)+'\n')

#read in the .cell file to get the proper format 
h=open(seedname+'.cell','r')
celllines=h.readlines()
h.close()

#look for the atomic positions in the cell file
for line in celllines:
	if '%block positions_abs' in line:
		beg_lineno = celllines.index(line)

#replace the initial atomic positions with the relaxed ones
for i in range(0,(len(coords))):
	celllines[i+beg_lineno+1]=coords[i]

#print out to new relaxed file 
g=open('relaxed_'+seedname+'.cell','w')
g.writelines(celllines)
g.close
