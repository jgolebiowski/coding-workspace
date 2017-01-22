#!/usr/bin/python
#------ This module operates on CASTEP output and input files
import sys

##############################################
#------ Classes
##############################################

class Atom:
	"""This is a class that stores the atomic data"""
	
	def __init__(self):
		self.x = None
		self.y = None
		self.z = None
		self.element = None
		self.index = None
		self.f_x = None
		self.f_y = None
		self.f_z = None
		self.force = None

class Structure:
	"""This is the class to hold a whole structure"""
	
	def __init__(self):
		self.lattice_vec = None
		self.atom_list = None


class Geomfile:
	"""Class that operates on .geom CASTEP files"""
	pass


##############################################
#------ Functions
##############################################

def get_xyz_positions(filename):
	f = open(filename, 'r')
	datalines = f.readlines()
	f.close

	atoms = []
	for line in datalines[2:]:
		new_atom = Atom()
		new_atom.element = line.split()[0]
		new_atom.x = float(line.split()[1])
		new_atom.y = float(line.split()[2])
		new_atom.z = float(line.split()[3])			

		atoms.append(new_atom)

	return atoms

def get_xyz_cell(atoms):
	x_lo = min([o.x for o in atoms])
	x_hi = max([o.x for o in atoms])
	y_lo = min([o.y for o in atoms])
	y_hi = max([o.y for o in atoms])
	z_lo = min([o.z for o in atoms])
	z_hi = max([o.z for o in atoms])


	for s_atom in atoms:
		s_atom.x -= x_lo
		s_atom.y -= y_lo
		s_atom.z -= z_lo
	x_hi -= (x_lo-0.1)
	y_hi -= (y_lo-0.1)
	z_hi -= (z_lo-0.1)

	cell_lattice_vectors = [ [0 for i in range(3)] for j in range(3)]
	
	cell_lattice_vectors[0][0] = x_hi
	cell_lattice_vectors[1][1] = y_hi
	cell_lattice_vectors[2][2] = z_hi

	return cell_lattice_vectors

def get_distance(atom1, atom2):
	distance = ((atom1.x - atom2.x)**2 + (atom1.y - atom2.y)**2 + (atom1.z - atom2.z)**2)**(0.5)
	return distance






from CASTEP_io_module_cellfile import *
from CASTEP_io_module_castepfile import *
