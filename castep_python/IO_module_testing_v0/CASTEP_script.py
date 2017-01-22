#!/usr/bin/python
#------ This module operates on CASTEP output and input files
import sys
from CASTEP_io_module import *
from CASTEP_io_module_cellfile import *



##############################################
#------ Main
##############################################
name_flakes = Cellfile('CNT_66_CDT_cluster_convergence-newcell.2_flakes.cell')
name_flakes.readdata()
"""
		self.filename=name
                self.k_points_spacing = None
                self.lattice_vec_lines = None
                self.lattice_vec = None
                self.atomic_position_lines = None
                self.atoms = None
                self.ionic_constraints = None
                self.extra_parameters = None
"""


name_flakes.get_celldata()
#print ''.join(name_flakes.atomic_position_lines)
name_flakes.get_atoms()
#name_flakes.atoms[0].x += 1
#name_flakes.update_atomic_lines()
#print ''.join(name_flakes.atomic_position_lines)

name_flakes.update_lattice_vectorlines()
#print ''.join(name_flakes.lattice_vec)
#print ''.join(name_flakes.atomic_position_lines)
#print ''.join(name_flakes.ionic_constraints)
#print ''.join(name_flakes.extra_parameters)
name_flakes.write_cell('test.cell')

test_structure = Structure()
name_flakes.populate_structure_class(test_structure)
#print test_structure.lattice_vectors
#print [o.x for o in test_structure.atom_list]

test_Atoms = get_xyz_positions('test_file.xyz')
test_vector = get_xyz_cell(test_Atoms)

new_cell = Cellfile()
new_cell.lattice_vec = test_vector
new_cell.atoms = test_Atoms

new_cell.update_atomic_lines()
new_cell.update_lattice_vectorlines()

new_cell.write_cell('supertest.cell')


#------ Cstepfilefile test

castepfile_test = Castepfilefile('CNT_66_CDT_cluster_convergence-newcell.2_flakes.castep')
castepfile_test.readdata()
castepfile_test.get_lattice_vectors()
castepfile_test.get_atomic_position_lines()
castepfile_test.get_atomic_positions()

