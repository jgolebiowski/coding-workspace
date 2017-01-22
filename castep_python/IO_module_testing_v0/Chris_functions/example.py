#!/usr/bin/python

# User defined Variables

string = 'Example text'
filename = 'example.txt'
newline = "new line\n"

# Script

f = open(filename,'r')
oldlines  = f.readlines()
f.close()
newlines = oldlines
for line in oldlines:
    if string in line:
        lineno = oldlines.index(line)
oldlines[lineno].split()[2] = str(float(oldlines[lineno].split()[2]) + 1) # Adds 1 to the 3rd word in the lineno line of oldlines
newlines[lineno] = newline
g = open(filename,'w')
g.writelines(newlines)
g.close()
