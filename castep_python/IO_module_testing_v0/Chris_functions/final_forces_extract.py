#!/usr/bin/python

#The code extracts a force on an addent and bond lenght+ mulliken population of d_1,6
import sys
import re

#open file as first parameter
seedname = str(sys.argv[1]) # First argument is a CASTEP seedname
force_expression=str(sys.argv[2]) #Second argument in the string indicting force
bond_expression = str(sys.argv[3]) # third argument in the string indicating bond in question

#print 'parameters elo elo melo',seedname,force_expression,bond_expression


#read in the file 
f=open(seedname+'.castep','r')
castlines = f.readlines()
f.close

#reverse the file to find the lst forces
rev_castlines=castlines[::-1]

#extract the line with force
for line in rev_castlines:
	if force_expression in line:
		forceline=line
		break
#extract the line with mulliken pop
for line in rev_castlines:
	if bond_expression in line:
		mullline=line

#extract the force, atomic distance and the mulliken population


bond_length=mullline.split()[6]
bond_population=mullline.split()[5]
add_force=re.findall('[-+]\d+.\d+', forceline.split()[3])[0]

print add_force+'\t'+bond_length+'\t'+bond_population
