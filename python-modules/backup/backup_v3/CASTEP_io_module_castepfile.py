#!/usr/bin/python
#------ This module operates on CASTEP output and input files
import sys

##############################################
#------ Classes
##############################################


class Castepfilefile:
	"""Class that operates on .castep CASTEP files"""
	
	def __init__(self, name = None):
                self.filename=name
                self.lattice_vec = None
                self.atoms = None
		self.atomic_lines = None
		self.force_lines = None

	def readdata(self, BFGS = False):

		if BFGS == False:
                	f = open(self.filename, 'r')
                	self.datalines = f.readlines()
                	f.close
		if BFGS == True:
			f = open(self.filename, 'r')
                        temp_datalines = f.readlines()
                        f.close

			for i in range( len( temp_datalines)):

				if 'Real Lattice(A)' in temp_datalines[i]:
					index_cell = i
					
				if 'BFGS : Final Configuration:' in temp_datalines[i]:
					index_BFGS = i
			self.datalines = temp_datalines[index_cell-3:index_cell+11]
			self.datalines += temp_datalines[index_BFGS-2:]

	def populate_structure_class(self, structure):
                """Fill in the data for a structure class"""
                if self.lattice_vec != None:
                        structure.lattice_vectors = self.lattice_vec
                if self.atoms != None:
                        structure.atom_list = self.atoms

	
	
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

	
	def get_force_lines(self):
                """Get the lines with atomic forces"""
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
                                        if '*********************** Forces ***********************' in self.datalines[i]:
                                                index_lines_beg = i
                                                flag_lines = True
                                else:
                                        if '******************************************************' in self.datalines[i]:
                                                index_lines_end = i
                                                flag_run = False

                self.force_lines = self.datalines[index_lines_beg+6:index_lines_end-1]


	def get_atomic_forces(self):
                """Get a proper list of atomic forces from forcelines"""

                if self.force_lines == None:
                        self.get_force_lines()

                for i in range(len(self.force_lines)):
			line = self.force_lines[i]
			atomic_index = line.split()[2]
			atomic_element = line.split()[1]
			
			force_x = float(line.split()[3])
			force_y = float(line.split()[4])
			force_z = float(line.split()[5])	
			
			self.atoms[i].f_x = force_x
			self.atoms[i].f_y = force_y
			self.atoms[i].f_z = force_z

			total_force = (force_x**2 + force_y**2 + force_z**2)**(0.5)
			self.atoms[i].force = total_force


from CASTEP_io_module import *
from CASTEP_io_module_cellfile import *

