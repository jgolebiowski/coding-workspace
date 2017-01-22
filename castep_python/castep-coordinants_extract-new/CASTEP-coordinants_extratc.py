#!/usr/bin/python
#------ This module operates on CASTEP output and input files
import sys
from CASTEP_io_module import *
from CASTEP_io_module_cellfile import *
from CASTEP_io_module_castepfile import *



##############################################
#------ Main
##############################################

name = str(sys.argv[1])
new_castepfile = Castepfilefile(name + '.castep')
new_castepfile.readdata(BFGS = True)
new_castepfile.get_lattice_vectors()
new_castepfile.get_atomic_positions()
system_data = Structure()
new_castepfile.populate_structure_class(system_data)

new_cellfile = Cellfile(name + '.cell')
new_cellfile.get_celldata()
new_cellfile.read_in_structure_class(system_data)
new_cellfile.update_atomic_lines()
new_cellfile.update_lattice_vectorlines()

new_cellfile.write_cell('relaxed-' + name + '.cell')

