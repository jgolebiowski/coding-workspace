#!/usr/bin/python

#this script cuts out a part of the animation
print "This is an .xyz animation cutter script, please run -h for help"

import sys
dump_file=str(sys.argv[1]) # first argument is the dump file seednam

if dump_file=='-h':
	exit("""Help:
	First argument is the dump file seedname
	Second argument is the animation start
	Third argument is the somulation stop
	Fourth argument is the iteration length
	!!! In order to print a single snaphot give 3 arguments !!!
	!!! 'Timestep no' 'Timestep no' 'Timesteo no' 		!!!""")

GLOB_start=int(sys.argv[2]) # Second argument is the animation start
GLOB_stop=int(sys.argv[3]) # Third argument is the somulation stop
GLOB_iter=int(sys.argv[4]) # Fourth argument is the iteration length 

if GLOB_start==GLOB_stop:
	GLOB_stop=GLOB_start+1
	GLOB_iter=GLOB_start+10

file=open(dump_file,'r')
dumplines=file.readlines()
file.close()

#numbers of start/stop timesteps
#GLOB_start=0
#GLOB_stop=2000
#GLOB_inter=200

for step in range(GLOB_start,GLOB_stop,GLOB_iter):
	T_start=step
	T_stop=step+GLOB_iter

	#Way to print a single snaphot 
	if GLOB_iter==GLOB_start+10:
		T_stop=T_start
	#----- Way to chop up corrupted runs
	if T_stop > GLOB_stop:
		T_stop = GLOB_stop

	start_string='Atoms. Timestep: '+str(T_start)
	stop_string='Atoms. Timestep: '+str(T_stop)
		
	#find the lines corresponding to the proper snapshots
	for line in dumplines:
		if start_string in line:
			start_no=int(dumplines.index(line)-1)
		if stop_string in line:
			stop_no=int(dumplines.index(line)+float(dumplines[dumplines.index(line)-1]))
			break
	
	
	animation=dumplines[start_no:stop_no+1]
	out_file=open(dump_file[:-4]+'-from-'+str(T_start)+'-to-'+str(T_stop)+'.xyz','w')
	out_file.writelines(animation)
	out_file.close


