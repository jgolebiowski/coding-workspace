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

class Structure:
	"""This is the class to hold a whole structure"""
	
	def __init__(self):
		self.lattice_vec = None
		self.atom_list = None


class Geomfile:
	"""Class that operates on .geom CASTEP files"""
	pass

class Castepfilefile:
	"""Class that operates on .castep CASTEP files"""
	
	def __init__(self, name = None):
                self.filename=name
                self.lattice_vec = None
                self.atoms = None
		self.atomic_lines = None

	def readdata(self, BFGS = False):

		if BFGS == False:
                	f = open(self.filename, 'r')
                	self.datalines = f.readlines()
                	f.close
	
	
	def get_lattice_vectors(self):
		"""Get the matrix of lattice vectors"""
		for i in range(len(self.datalines)):
			if 'Real Lattice(A)' in self.datalines[i]:
				lattice_lines = self.datalines[i+1:i+4]
				break

		self.lattice_vec = [ [0 for i in range(3)] for i in range(3)]
	
                for i in range(3):
                        self.lattice_vec[i][0] = float(lattice_lines[i].split()[0])
                        self.lattice_vec[i][1] = float(lattice_lines[i].split()[1])
                        self.lattice_vec[i][2] = float(lattice_lines[i].split()[2])




		
        def get_atomic_position_lines(self):
		"""Get the lines with atomic positions"""
		flag_cell_content = False
		flag_lines = False
		flag_run = True
		
		for i in range(len(self.datalines)):
			if flag_run == False:
				break
			if flag_cell_content == False:
				if 'Cell Contents' in self.datalines[i]:
					index_cell_content = i
					flag_cell_content = True
			else:
				if flag_lines == False:
					if 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' in self.datalines[i]:
						index_lines_beg = i
						flag_lines = True
				else:
					if 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' in self.datalines[i]:
						index_lines_end = i
						flag_run = False

		self.atomic_lines = self.datalines[index_lines_beg+4:index_lines_end]

	def get_atomic_positions(self):
		"""Get a proper list of atoms from the atomic positions"""
		self.atoms = []
		
		if self.atomic_lines == None:
			self.get_atomic_position_lines()
	
		for line in self.atomic_lines:
			new_atom = Atom()
			new_atom.index = line.split()[2]
			new_atom.element = line.split()[1]
			new_atom.x = float(line.split()[3]) * self.lattice_vec[0][0] + float(line.split()[4]) * self.lattice_vec[0][1] + float(line.split()[5]) * self.lattice_vec[0][2]
			new_atom.y = float(line.split()[3]) * self.lattice_vec[1][0] + float(line.split()[4]) * self.lattice_vec[1][1] + float(line.split()[5]) * self.lattice_vec[1][2]
			new_atom.z = float(line.split()[3]) * self.lattice_vec[2][0] + float(line.split()[4]) * self.lattice_vec[2][1] + float(line.split()[5]) * self.lattice_vec[2][2]
			
			self.atoms.append(new_atom)

	


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


from CASTEP_io_module_cellfile import *
