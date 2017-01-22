#!/usr/bin/python

import numpy as np

# Extract index of last line in list at which string occurs. Within optional min-max range.
def strindex(list,string,nmin=0,nmax=0):
    if nmax == 0:
        nmax = len(list)
    i = 0
    for item in list:
        if string in item:
            if i >= nmin and i <= nmax:
                index = i
        i = i+1
    return index

# Extract list of indicies of lines in list at which string occurs. Within optional min-max range.
def strindicies(list,string,nmin=0,nmax=0):
    if nmax == 0:
        nmax = len(list)
    indicies = []
    i = 0
    for item in list:
        if string in item:
            if i >= nmin and i <= nmax:
                indicies.append(i)
        i = i+1
    return indicies

# Extract number of ions from .phonon file
def get_no_ions(flines):
    nions = strindex(flines,'Number of ions')
    N = int(flines[nions].split()[3])
    return N

# Extract lattice vectors from .phonon file
def get_lat_vecs(flines):
    nlat = strindex(flines,'Unit cell vectors (A)')
    avec = [float(flines[nlat+1].split()[0]),float(flines[nlat+1].split()[1]),float(flines[nlat+1].split()[2])]
    bvec = [float(flines[nlat+2].split()[0]),float(flines[nlat+2].split()[1]),float(flines[nlat+2].split()[2])]
    cvec = [float(flines[nlat+3].split()[0]),float(flines[nlat+3].split()[1]),float(flines[nlat+3].split()[2])]
    latvec = [avec, bvec, cvec]
    return latvec

# Extract ion positions from .phonon file
def get_ion_posns(flines,Nions):
    latvec = get_lat_vecs(flines)
    npos = strindex(flines,'Fractional Co-ordinates') + 1
    fracposns = []
    for i in range(0,Nions):
        line = flines[npos+i]
        pos = [float(line.split()[1]),float(line.split()[2]),float(line.split()[3])]
        fracposns.append(pos)
    posns = []
    for fpos in fracposns:
        posns.append(np.dot(latvec,fpos))
    return posns

# Extract elements from .phonon file
def get_elements(flines,Nions):
    npos = strindex(flines,'Fractional Co-ordinates') + 1
    elements = []
    for i in range(0,Nions):
        line = flines[npos+i]
        elements.append(line.split()[4])
    return elements

# Extracts phonon eigenvectors from .phonon file
def get_eigvects(flines,Nions,branch,qpt):
    nqpts = strindicies(flines,'q-pt=')
    nqpoint = 0
    for nqpt in nqpts:
        if float(flines[nqpt].split()[2])==qpt[0] and float(flines[nqpt].split()[3])==qpt[1] and float(flines[nqpt].split()[4])==qpt[2]:
            nqpoint = nqpt
    if nqpoint == 0:
        print "Requested q-point: " + ' '.join([str(q) for q in qpt]) + " does not appear in output file.\nPlease request a different set of q-points."
        exit()
    if nqpts.index(nqpoint) == len(nqpts)-1:
        nqmax = len(flines)
    else:
        nqmax = nqpts[nqpts.index(nqpoint)+1]
    nvectsstart = strindex(flines,'Phonon Eigenvectors',nmin=nqpoint,nmax=nqmax)
    nbranch = nvectsstart + 2 + int(branch-1)*int(Nions)
    i = 0
    eigvects = []
    while i < Nions:
        line = flines[nbranch+i]
        vect = [float(line.split()[2]),float(line.split()[4]),float(line.split()[6])]
        eigvects.append(vect)
        i = i + 1
    return eigvects

# Appends vertically one numpy array (array2) to a first (array1) even if array1 is empty
def npvstack(array1,array2):
    if len(array1) == 0:
        array1 = array2
    else:
        array1 = np.vstack((array1,array2))
    return array1

# Prints a castep .cell file with absolute atomic positions
def createcell(printcell,latvecs,elements,sumposns):
    cell = []
    pos_digit = 16               # Number of decimal places in atom posns
    string = "{0:." + str(pos_digit) + "f}"
    cell.append('%BLOCK LATTICE_CART\n')
    cell.append(str(string.format(latvecs[0][0]))+'\t'+str(string.format(latvecs[0][1]))+'\t'+str(string.format(latvecs[0][2]))+'\n')
    cell.append(str(string.format(latvecs[1][0]))+'\t'+str(string.format(latvecs[1][1]))+'\t'+str(string.format(latvecs[1][2]))+'\n')
    cell.append(str(string.format(latvecs[2][0]))+'\t'+str(string.format(latvecs[2][1]))+'\t'+str(string.format(latvecs[2][2]))+'\n')
    cell.append('%ENDBLOCK LATTICE_CART\n')
    cell.append('\n')
    cell.append('%BLOCK POSITIONS_ABS\n')
    i = 0
    for element in elements:
        cell.append(element+'\t'+str(string.format(sumposns[i][0]))+'\t'+str(string.format(sumposns[i][1]))+'\t'+str(string.format(sumposns[i][2]))+'\n')
        i = i+1
    cell.append('%ENDBLOCK POSITIONS_ABS\n')
    f = open(printcell,'w')
    f.writelines( cell )
    f.close()
    return
