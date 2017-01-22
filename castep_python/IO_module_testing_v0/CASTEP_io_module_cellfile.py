#!/usr/bin/python
#------ This module operates on CASTEP output and input files
import sys

##############################################
#------ Classes
##############################################

class Cellfile:
	"""Class that operates on .cell CASTEP files"""

	def __init__(self, name=None):
		self.filename=name
		self.k_points_spacing = None
		self.lattice_vec_lines = None
		self.lattice_vec = None
		self.atomic_position_lines = None
		self.atoms = None
		self.ionic_constraints = None
		self.extra_parameters = None

	def readdata(self):
		f = open(self.filename, 'r')
		self.datalines = f.readlines()
		f.close
	def get_k_points(self):
		"""Get the k points spacing from the cell"""
		index=-1
		for line in self.datalines:
			index=index+1
			if 'kpoints_mp_grid' in line:
				if len(line.split()) == 5:
					shift=1
				else:
					shift=0
				k_x=line.split()[1+shift]
				k_y=line.split()[2+shift]
				k_z=line.split()[3+shift]
				self.k_points_spacing=[k_x, k_y, k_z]
	def get_lattice_vec(self):
		"""Get the cell vectors"""
		index=-1
		for line in self.datalines:
			index=index+1
			if '%block lattice_cart' in line or '%BLOCK LATTICE_CART' in line:
				lattice_beg=iteration=index+2
			if '%endblock lattice_cart' in line or '%ENDBLOCK LATTICE_CART' in line:
				lattice_end=index
		self.lattice_vec_lines = self.datalines[lattice_beg:lattice_end]

		self.lattice_vec = [ [0 for i in range(3)] for i in range(3)]
		for i in range(3):
			self.lattice_vec[i][0] = float(self.lattice_vec_lines[i].split()[0])
			self.lattice_vec[i][1] = float(self.lattice_vec_lines[i].split()[1])
			self.lattice_vec[i][2] = float(self.lattice_vec_lines[i].split()[2])

	def update_lattice_vectorlines(self):
		"""Update vectorlines with the data stored in lattice_vec"""
		
		if self.lattice_vec == None:
			raise Exception("No lattice cell vectors found")
		
		self.lattice_vec_lines = [0, 0, 0]
		for i in range(3):
			
			x = str(self.lattice_vec[i][0])
			y = str(self.lattice_vec[i][1])
			z = str(self.lattice_vec[i][2])
			self.lattice_vec_lines[i]=x+'\t'+y+'\t'+z+'\n'
	
	def get_atomic_position_lines(self):
		"""Get the atomic positions"""
                index=-1
                for line in self.datalines:
                        index=index+1
			if '%block positions' in line or '%BLOCK POSITIONS' in line:
				atomic_beg = index+1
			if '%endblock positions' in line or '%ENDBLOCK POSITIONS'in line:
				atomic_end = index
		self.atomic_position_lines = self.datalines[atomic_beg:atomic_end]
	
	def get_atoms(self):
		"""populate the atoms"""
		self.atoms = []
		if self.atomic_position_lines == None:
                        self.get_atomic_position_lines()
	
		for line in self.atomic_position_lines:
			new_atom = Atom()
			new_atom.x = float(line.split()[1])
			new_atom.y = float(line.split()[2])
			new_atom.z = float(line.split()[3])
			new_atom.element = line.split()[0]
			self.atoms.append(new_atom)

	def update_atomic_lines(self):
		"""Update the atomic lines according to atoms"""
		if self.atoms == None:
			self.get_atoms()
		
		self.atomic_position_lines = []
		for single_atom in self.atoms:
			element = single_atom.element
			x = str(single_atom.x)
			y = str(single_atom.y)
			z = str(single_atom.z)
			self.atomic_position_lines.append(element+'\t'+x+'\t'+y+'\t'+z+'\n')




	def get_ionic_constraints(self):
		"""Get the atomic constraints"""
		index=-1
		constraints_beg = None

                for line in self.datalines:
                        index=index+1
                        if '%block ionic_constraints' in line or '%BLOCK IONIC_CONSTRAINTS' in line:
                                constraints_beg = index+1
                        if '%endblock ionic_constraints' in line or '%ENDBLOCK IONIC_CONSTRAINTS'in line:
                                constraints_end = index

		if constraints_beg == None:
			self.ionic_constraints = None
		else:
                	self.ionic_constraints=self.datalines[constraints_beg:constraints_end]

	def get_extra_parameters(self):
		"""Get any other parameters from the cell file"""
		index=-1
		extra_p_beg = None
                for line in self.datalines:
                        index=index+1
                        if '%endblock ionic_constraints' in line or '%ENDBLOCK IONIC_CONSTRAINTS'in line:
                                extra_p_beg = index+1
		if extra_p_beg == None:
			self.extra_parameters = None
		else:
			self.extra_parameters=self.datalines[extra_p_beg:]

	def get_celldata(self):
		"""Populate the cell file with the get_ functions"""
		if self.k_points_spacing == None:
			self.get_k_points()
		if self.lattice_vec_lines == None:
			self.get_lattice_vec()
		if self.atomic_position_lines == None:
			self.update_atomic_lines()
		if self.ionic_constraints == None:
			self.get_ionic_constraints()
		if self.extra_parameters == None:
			self.get_extra_parameters()

	def populate_structure_class(self, structure):
		"""Fill in the data for a structure class"""
		if self.lattice_vec != None:
			structure.lattice_vectors = self.lattice_vec
		if self.atoms != None:
			structure.atom_list = self.atoms

	def interlude(self,string):
		strline='!!! '+str(string)+'\n'
		result=[]
		result.append('\n')
		result.append('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
		result.append(strline)
		result.append('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
		result.append('\n')
		return result

	def write_cell(self,name=None):
		if name == None:
			name='second'+self.filename
		
		if self.k_points_spacing == None:
                        self.k_points_spacing = [1, 1, 1]
                if self.lattice_vec_lines == None:
                        self.lattice_vec_lines = ['\n']
                if self.atomic_position_lines == None:
                        self.atomic_position_lines = ['\n']

		output = self.interlude('This is a CASTEP .cell file created by Jacek')
		output =  output + ['! -------- File begins below\n']
		output =  output + self.interlude('Size of k-point mesh')

		kline='kpoints_mp_grid = '+str(self.k_points_spacing[0])+' '+str(self.k_points_spacing[1])+' '+str(self.k_points_spacing[2])+'\n'
		output.append(kline)
		output = output + self.interlude('Lattice vector in cartesian coordinants')
		output = output+['%block lattice_cart\n','ang\n']+self.lattice_vec_lines+['%endblock lattice_cart\n','\n']

		output = output + self.interlude('Atomic positions in absolute units')
		output = output+['%block positions_abs\n']+self.atomic_position_lines+['%endblock positions_abs\n','\n']
		if self.ionic_constraints == None:
                        output = output + ['\n']
		else:
			output = output + self.interlude('Ionic constraints')
			output = output+['%block ionic_constraints\n']+self.ionic_constraints+['%endblock ionic_constraints\n','\n']
		
		if self.extra_parameters == None:
                        output += ['\n']
		else:
			output = output + self.interlude('Extra parameters')
			output = output + self.extra_parameters

		g = open(name, 'w')
		g.writelines(output)
		g.close

from CASTEP_io_module import *

