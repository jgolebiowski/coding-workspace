#!/usr/bin/python

#this script slices a cell in half
print "This is an .xyz cell slicer, please run -h for help"

import sys
dump_file=str(sys.argv[1]) # first argument is the dump file seednam
if dump_file=='-h':
        exit("""Help:
        First argument is the dump file seedname
        Second argument is the position of the slice in X""")


#give the position of a slice
pos_slice=float(sys.argv[2])


file=open(dump_file,'r')
dumplines=file.readlines()
file.close()

rev_dumplines=dumplines[::-1] #reverse lines
rev_snapshot=[] #find the lines corresponding to the last snapshot

#flag=0
for line in rev_dumplines:
	rev_snapshot.append(line)
#	if flag==1:
#		break
	if 'Timestep' in line:
#		flag=1
		atom_no=rev_dumplines[rev_dumplines.index(line)+1]
		rev_snapshot.append(atom_no)
		break
		
snapshot=rev_snapshot[::-1]

cell_slice=[] #getting the slice 
for line in snapshot[2:]:
	pos_x=float(line.split()[1])
	if pos_x <= pos_slice:
		cell_slice.append(line)

#add necessary xyz lines
cell_slice.insert(0,'This is the cell slice for a final configuration\n')
cell_slice.insert(0,str(len(cell_slice)-1)+'\n')


#print out the new file 
out_file=open(dump_file[:-4]+'_sliced.xyz','w')
out_file.writelines(cell_slice)
out_file.close
