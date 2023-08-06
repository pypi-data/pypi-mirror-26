from __future__ import absolute_import
from __future__ import print_function
from .Util import *
import numpy as np
import random, math
from .Mol import *
from .Electrostatics import *

def Submit_Script_Lines(order=str(3), sub_order =str(1), index=str(1), mincase = str(0), maxcase = str(1000), name = "MBE", ncore = str(4), queue="long"):
	lines = "#!/bin/csh\n"+"# Submit a job for 8  processors\n"+"#$ -N "+name+"\n#$ -t "+mincase+"-"+maxcase+":1\n"+"#$ -pe smp "+ncore+"\n"+"#$ -r n\n"+"#$ -q "+queue+"\n\n\n"
	lines += "module load gcc/5.2.0\nsetenv  QC /afs/crc.nd.edu/group/parkhill/qchem85\nsetenv  QCAUX /afs/crc.nd.edu/group/parkhill/QCAUX_1022\nsetenv  QCPLATFORM LINUX_Ix86\n\n\n"
	lines += "/afs/crc.nd.edu/group/parkhill/qchem85/bin/qchem  -nt "+ncore+"   "+str(order)+"/"+"${SGE_TASK_ID}/"+sub_order+"/"+index+".in  "+str(order)+"/"+"${SGE_TASK_ID}/"+sub_order+"/"+index+".out\n\nrm MBE*.o*"
	return lines

def String_To_Atoms(s=""):
	l = list(s)
	atom_l = []
	tmp = ""
	for i, c in enumerate(l):
		if  ord('A') <= ord(c) <= ord('Z'):
			tmp=c
		else:
			tmp += c
		if i==len(l)-1:
			atom_l.append(tmp)
		elif ord('A') <= ord(l[i+1]) <= ord('Z'):
			atom_l.append(tmp)
		else:
			continue
	return atom_l

def Binominal_Combination(indis=[0,1,2], group=3):
	if (group==1):
		index=list(itertools.permutations(indis))
		new_index =[]
		for i in range (0, len(index)):
			new_index.append(list(index[i]))
		return new_index
	else:
		index=list(itertools.permutations(indis))
		new_index=[]
		for sub_list in Binominal_Combination(indis, group-1):
			for sub_index in index:
				new_index.append(list(sub_list)+list(sub_index))
		return new_index

class FragableCluster(Mol):
	""" Provides a cluster which can be fragmented into molecules"""
	def __init__(self, atoms_ =  None, coords_ = None):
		Mol.__init__(self,atoms_,coords_)
		self.mbe_order = PARAMS["MBE_ORDER"]
		self.frag_list = []    # list of [{"atom":.., "charge":..},{"atom":.., "charge":..},{"atom":.., "charge":..}]
		self.type_of_frags = []  # store the type of frag (1st order) in the self.mbe_frags:  [1,1,1 (H2O), 2,2,2(Na),3,3,3(Cl)]
		self.type_of_frags_dict = {}
		self.atoms_of_frags = [] # store the index of atoms of each frag
		self.mbe_frags=dict()    # list of  frag of each order N, dic['N'=list of frags]
		self.mbe_frags_deri=dict()
		self.mbe_frags_energy=dict()  # MBE energy of each order N, dic['N'= E_N]
		self.mbe_energy=dict()   # sum of MBE energy up to order N, dic['N'=E_sum]
		self.mbe_deri =None
		self.ngroup=None
		return

	def Reset_Frags(self):
		self.mbe_frags=dict()    # list of  frag of each order N, dic['N'=list of frags]
		self.mbe_frags_deri=dict()
		self.mbe_permute_frags=dict() # list of all the permuted frags
		self.mbe_frags_energy=dict()  # MBE energy of each order N, dic['N'= E_N]
		self.energy=None
		self.mbe_energy=dict()   # sum of MBE energy up to order N, dic['N'=E_sum]
		self.mbe_deri =None
		self.nn_energy=None
		return

	def Sort_frag_list(self):
		a=[]
		for dic in self.frag_list:
			a.append(len(dic["atom"]))
		self.frag_list = [x for (y,x) in sorted(zip(a,self.frag_list))]
		self.frag_list.reverse()
		return self.frag_list

	def Generate_All_Pairs(self, pair_list=[]):
		mono = []
		for pair in pair_list:
			for frag in pair['mono']:
				mono.append([atoi[atom] for atom in  String_To_Atoms(frag)])
		tmp = []
		for frag in mono:
			if frag not in tmp:
				tmp.append(frag)
		mono = tmp
		mono.sort(key=lambda x:len(x))
		mono.reverse()
		dic_mono = {}
		dic_mono_index = {}
		masked = []
		for frag_atoms in mono:
			frag_name = LtoS(frag_atoms)
			dic_mono[frag_name] = []
			dic_mono_index[frag_name] = []
			num_frag_atoms = len(frag_atoms)
			j = 0
			while (j < self.NAtoms()):
				if j in masked:
					j += 1
				else:
					tmp_list = list(self.atoms[j:j+num_frag_atoms])
					if tmp_list == frag_atoms:
						dic_mono[frag_name].append(self.coords[j:j+num_frag_atoms,:].copy())
						dic_mono_index[frag_name].append(range (j, j+num_frag_atoms))
						masked += range (j, j+num_frag_atoms)
						j += num_frag_atoms
					else:
						j += 1
		happy_atoms = []
		for pair in pair_list:
			happy_atoms = self.PairUp(dic_mono, dic_mono_index, pair, happy_atoms)  #it is amazing that the dictionary is passed by pointer...
		left_atoms = list(set(range (0, self.NAtoms())) - set(happy_atoms))
		sorted_atoms = happy_atoms + left_atoms
		self.atoms = self.atoms[sorted_atoms]
		self.coords = self.coords[sorted_atoms]
		return

	def PairUp(self, dic_mono, dic_mono_index, pair, happy_atoms):  # stable marriage pairing  Ref: https://en.wikipedia.org/wiki/Stable_marriage_problem
		mono_1 = LtoS([atoi[atom] for atom in  String_To_Atoms(pair["mono"][0])])
		mono_2 = LtoS([atoi[atom] for atom in  String_To_Atoms(pair["mono"][1])])
		center_1 = pair["center"][0]
		center_2 = pair["center"][1]
		switched = False
		if len(dic_mono[mono_1]) > len(dic_mono[mono_2]):
			mono_1, mono_2 = mono_2, mono_1
			center_1, center_2  = center_2, center_1
			switched = True
		mono_1_pair = [-1]*len(dic_mono[mono_1])
		dist_matrix = np.zeros((len(dic_mono[mono_1]), len(dic_mono[mono_2])))
		for i in range (0, len(dic_mono[mono_1])):
			for j in range (0, len(dic_mono[mono_2])):
				dist_matrix[i][j] = np.linalg.norm(dic_mono[mono_1][i][center_1] - dic_mono[mono_2][j][center_2])
		mono_1_prefer = []
		mono_2_prefer = []
		for i in range (0, len(dic_mono[mono_1])):
			s = list(dist_matrix[i])
			mono_1_prefer.append(sorted(range(len(s)), key=lambda k: s[k]))
		for i in range (0, len(dic_mono[mono_2])):
			s = list(dist_matrix[:,i])
			mono_2_prefer.append(sorted(range(len(s)), key=lambda k: s[k]))
		mono_1_info = [-1]*len(dic_mono[mono_1]) # -1 means they are not paired, and the number means the Nth most prefered are chosen
		mono_2_info = [-1]*len(dic_mono[mono_2])
		mono_1_history = [0]*len(dic_mono[mono_1]) # history of the man's proposed
		# first round  mono_1 is the man, mono_2 is woman,  num of man > num of woman
		for i in range (0, len(dic_mono[mono_1])):
			target = mono_1_prefer[i][0]
			if i == mono_2_prefer[target][0]:  # Congs! find true lovers
				mono_1_info[i] = 0
				mono_2_info[target] = 0
			mono_1_history[i] += 1
		while (-1 in mono_1_info):
			for i in range (0, len(dic_mono[mono_1])):
				if mono_1_info[i] == -1:
					target = mono_1_prefer[i][mono_1_history[i]] # propose
					if mono_2_info[target] == -1: # met a single woman
						mono_1_info[i] = mono_1_history[i]
						mono_2_info[target] = mono_2_prefer[target].index(i)
						mono_1_history[i] += 1
					elif mono_2_info[target] > mono_2_prefer[target].index(i):   # this man is the better choice than the previous one
						poorguy = mono_2_prefer[target][mono_2_info[target]]
						mono_1_info[poorguy] = -1   # this poor guy is abandoned...
						mono_1_info[i] = mono_1_history[i]
						mono_2_info[target] = mono_2_prefer[target].index(i)
						mono_1_history[i] += 1
					else:
						mono_1_history[i] += 1
						continue
				else:
					continue
		final_pairs = []
		for i in range (0, len(dic_mono[mono_1])):
			final_pairs.append([i, mono_1_prefer[i][mono_1_info[i]]])
		for i in range (0, len(final_pairs)):
			if switched == False:
				#print dic_mono_index[mono_1][final_pairs[i][0]], dic_mono_index[mono_2][final_pairs[i][1]]
				happy_atoms += dic_mono_index[mono_1][final_pairs[i][0]]
				happy_atoms += dic_mono_index[mono_2][final_pairs[i][1]]
			else:
				happy_atoms += dic_mono_index[mono_2][final_pairs[i][1]]
				happy_atoms += dic_mono_index[mono_1][final_pairs[i][0]]
		indices_1 = [item[0] for item in final_pairs]
		indices_2 = [item[1] for item in final_pairs]
		dic_mono_index[mono_1] = [i for j, i in enumerate(dic_mono_index[mono_1]) if j not in indices_1]
		dic_mono_index[mono_2] = [i for j, i in enumerate(dic_mono_index[mono_2]) if j not in indices_2]
		dic_mono[mono_1] = [i for j, i in enumerate(dic_mono[mono_1]) if j not in indices_1]
		dic_mono[mono_2] = [i for j, i in enumerate(dic_mono[mono_2]) if j not in indices_2]
		#print dic_mono_index[mono_1], dic_mono_index[mono_2], happy_atoms
		return happy_atoms

	def Generate_All_MBE_term_General(self, frag_list=[], cutoff=10, center_atom=[]):
		self.frag_list = frag_list
		#self.Sort_frag_list()  # debug, not sure it is necessary
		if center_atom == []:
			center_atom = [0]*len(frag_list)
		for i in range (1, self.mbe_order+1):
			print("Generating order", i)
			self.Generate_MBE_term_General(i, cutoff, center_atom)
		return

	def Generate_MBE_term_General(self, order,  cutoff=10, center_atom=[]):
		if order in self.mbe_frags.keys():
			print(("MBE order", order, "already generated..skipping.."))
			return
		if order==1:
			self.mbe_frags[order] = []
			masked=[]
			frag_index = 0
			# Generating MBE frags with stable marriage
			for i, dic in enumerate(self.frag_list):
				self.type_of_frags_dict[i] = []
				frag_atoms = String_To_Atoms(dic["atom"])
				frag_atoms = [atoi[atom] for atom in frag_atoms]
				num_frag_atoms = len(frag_atoms)
				j = 0
				while (j < self.NAtoms()):
					if j in masked:
						j += 1
					else:
						tmp_list = list(self.atoms[j:j+num_frag_atoms])
						if tmp_list == frag_atoms:
							self.atoms_of_frags.append([])
							masked += range (j, j+num_frag_atoms)
							self.atoms_of_frags[-1]=range (j, j+num_frag_atoms)
							self.type_of_frags.append(i)
							self.type_of_frags_dict[i].append(frag_index)
							tmp_coord = self.coords[j:j+num_frag_atoms,:].copy()
							tmp_atom  = self.atoms[j:j+num_frag_atoms].copy()
							mbe_terms = [frag_index]
							mbe_dist = None
							atom_group = [num_frag_atoms]
							dic['num_electron'] = sum(list(tmp_atom))-dic['charge']
							frag_type = [dic]
							frag_type_index = [i]
							tmp_mol = Frag(tmp_atom, tmp_coord, mbe_terms, mbe_dist, atom_group, frag_type, frag_type_index, FragOrder_=order)
							self.mbe_frags[order].append(tmp_mol)
							j += num_frag_atoms
							frag_index += 1
							#print self.atoms_of_frags, tmp_list, self.type_of_frags
							#print self.mbe_frags[order][-1].atoms, self.mbe_frags[order][-1].coords, self.mbe_frags[order][-1].index
						else:
							j += 1
		else:
			num_of_each_frag = {}
			frag_list_length = len(self.frag_list)
			frag_list_index = range (0, frag_list_length)
			frag_list_index_list = list(itertools.product(frag_list_index, repeat=order))
			tmp_index_list = []
			for i in range (0, len(frag_list_index_list)):
				tmp_index = list(frag_list_index_list[i])
				tmp_index.sort()
				if tmp_index not in tmp_index_list:
					tmp_index_list.append(tmp_index)
					num_of_each_frag[LtoS(tmp_index)]=0
			self.mbe_frags[order] = []
			mbe_terms=[]
			mbe_dist=[]
			ngroup = len(self.mbe_frags[1])	#
			atomlist=list(range(0,ngroup))
			time_log = time.time()
			print(("generating the combinations for order: ", order))
			max_case = 5000
			time_now=time.time()
			for index_list in tmp_index_list:
				frag_case = 0
				sample_index = []
				for i in index_list:
					sample_index.append(self.type_of_frags_dict[i])
				print("begin the most time consuming step: ")
				tmp_time  = time.time()
				sub_combinations = list(itertools.product(*sample_index))
				print(("end of the most time consuming step. time cost:", time.time() - tmp_time))
				#shuffle_time = time.time()
				#new_begin = random.randint(1,len(sub_combinations)-2)
				#sub_combinations = sub_combinations[new_begin:]+sub_combinations[:new_begin] # debug, random shuffle the list, so the pairs are chosen randomly, this is not necessary for generate training cases
				#random.shuffle(sub_combinations)  # debug, random shuffle the list, so the pairs are chosen randomly, this is not necessary for generate training cases
				#print  "time to shuffle it", time.time()-shuffle_time
				for i in range (0, len(sub_combinations)):
					term = list(sub_combinations[i])
					if len(list(set(term))) < len(term):
						continue
					pairs=list(itertools.combinations(term, 2))
					saveindex=[]
					dist = [float('inf')]*len(pairs)
					flag=1
					npairs=len(pairs)
					for j in range (0, npairs):
						#print self.type_of_frags[pairs[j][0]], self.type_of_frags[pairs[j][1]], pairs[j][0], pairs[j][1]
						if self.type_of_frags[pairs[j][0]] == -1 :
							center_1 = self.Center()
						else:
							center_1 = self.mbe_frags[1][pairs[j][0]].coords[center_atom[self.type_of_frags[pairs[j][0]]]]
						if self.type_of_frags[pairs[j][1]] == -1 :
							center_2 = self.Center()
						else:
							center_2 = self.mbe_frags[1][pairs[j][1]].coords[center_atom[self.type_of_frags[pairs[j][1]]]]
						dist[j] = np.linalg.norm(center_1- center_2)
						if dist[j] > cutoff:
							flag = 0
							break
					if flag == 1:   # we find a frag
						if frag_case%100==0:
							print("working on frag:", frag_case, "frag_type:", index_list, " i:", i)
						frag_case  += 1
						if  frag_case >=  max_case:   # just for generating training case
							break;
						mbe_terms.append(term)
						mbe_dist.append(dist)
			print(("finished..takes", time_log-time.time(),"second"))
			mbe_frags = []
			for i in range (0, len(mbe_terms)):
				frag_type = []
				frag_type_index = []
				atom_group = []
				for index in mbe_terms[i]:
					frag_type.append(self.frag_list[self.type_of_frags[index]])
					frag_type_index.append(self.type_of_frags[index])
					atom_group.append(self.mbe_frags[1][index].atoms.shape[0])
				tmp_coord = np.zeros((sum(atom_group), 3))
				tmp_atom = np.zeros(sum(atom_group), dtype=np.uint8)
				pointer = 0
				for j, index in enumerate(mbe_terms[i]):
					tmp_coord[pointer:pointer+atom_group[j],:] = self.mbe_frags[1][index].coords
					tmp_atom[pointer:pointer+atom_group[j]] = self.mbe_frags[1][index].atoms
					pointer += atom_group[j]
				tmp_mol = Frag(tmp_atom, tmp_coord, mbe_terms[i], mbe_dist[i], atom_group, frag_type, frag_type_index, FragOrder_=order)
				self.mbe_frags[order].append(tmp_mol)
			# completed self.mbe_frags
			del sub_combinations
		return

	def Calculate_Frag_Energy_General(self, order, method="pyscf"):
		if order in self.mbe_frags_energy.keys():
			print(("MBE order", order, "already calculated..skipping.."))
			return 0
		mbe_frags_energy = 0.0
		fragnum=0
		time_log=time.time()
		if method == "qchem":
			order_path = self.qchem_data_path+"/"+str(order)
			if not os.path.isdir(order_path):
				os.mkdir(order_path)
			os.chdir(order_path)
			time0 =time.time()
			for frag in self.mbe_frags[order]:  # just for generating the training set..
				fragnum += 1
				if fragnum%100 == 0:
					print("working on frag:", fragnum)
					print("total time:", time.time() - time0)
				time0 = time.time()
				frag.Write_Qchem_Frag_MBE_Input_All_General(fragnum)
			os.chdir("../../../..")
		elif method == "pyscf":
			for frag in self.mbe_frags[order]:
				fragnum += 1
				print("doing the ",fragnum)
				frag.PySCF_Frag_MBE_Energy_All()
				frag.Set_Frag_MBE_Energy()
				mbe_frags_energy += frag.frag_mbe_energy
			print("Finished, spent ", time.time()-time_log," seconds")
			time_log = time.time()
			self.mbe_frags_energy[order] = mbe_frags_energy
		else:
			raise Exception("unknow ab-initio software!")
		return

	def Get_Qchem_Frag_Energy(self, order):
		fragnum = 0
		path = self.qchem_data_path+"/"+str(order)
		mbe_frags_energy = 0.0
		for frag in self.mbe_frags[order]:
			fragnum += 1
			frag.Get_Qchem_Frag_MBE_Energy_All(fragnum, path)
			print("working on molecule:", self.name," frag:",fragnum, " order:",order)
			frag.Set_Frag_MBE_Energy()
			mbe_frags_energy += frag.frag_mbe_energy
			#if order==2:
		#		print frag.frag_mbe_energy, frag.dist[0]
		self.mbe_frags_energy[order] = mbe_frags_energy
		return

	def Get_All_Qchem_Frag_Energy_General(self):
		for i in range (1, self.mbe_order+1):
			self.Get_Qchem_Frag_Energy(i)
		return

	def Calculate_All_Frag_Energy_General(self, method="pyscf"):
		if method == "qchem":
			if not os.path.isdir("./qchem"):
				os.mkdir("./qchem")
			if not os.path.isdir("./qchem"+"/"+self.properties["set_name"]):
				os.mkdir("./qchem"+"/"+self.properties["set_name"])
			self.qchem_data_path="./qchem"+"/"+self.properties["set_name"]+"/"+self.name
			print("set_name",  self.properties["set_name"], " self.name", self.name)
			if not os.path.isdir(self.qchem_data_path):
				os.mkdir(self.qchem_data_path)
		for i in range (1, self.mbe_order+1):
			print("calculating for MBE order", i)
			self.Calculate_Frag_Energy_General(i, method)
		if method == "qchem":
			self.Write_Qchem_Submit_Script()
		return

	def Write_Qchem_Submit_Script(self):     # this is for submitting the jobs on notre dame crc
		if not os.path.isdir("./qchem"):
			os.mkdir("./qchem")
			if not os.path.isdir("./qchem"+"/"+self.properties["set_name"]):
				os.mkdir("./qchem"+"/"+self.properties["set_name"])
				self.qchem_data_path="./qchem"+"/"+self.properties["set_name"]+"/"+self.name
		if not os.path.isdir(self.qchem_data_path):
			os.mkdir(self.qchem_data_path)
		os.chdir(self.qchem_data_path)
		for i in range (1, self.mbe_order+1):
			num_frag = len(self.mbe_frags[i])
			for j in range (1, i+1):
				index=nCr(i, j)
				for k in range (1, index+1):
					submit_file = open("qchem_order_"+str(i)+"_suborder_"+str(j)+"_index_"+str(k)+".sub","w+")
					lines = Submit_Script_Lines(order=str(i), sub_order =str(j), index=str(k), mincase = str(1), maxcase = str(num_frag), name = "MBE_"+str(i)+"_"+str(j)+"_"+str(index), ncore = str(4), queue="long")
					submit_file.write(lines)
					submit_file.close()

		python_submit = open("submit_all.py","w+")
		line = 'import os,sys\n\nfor file in os.listdir("."):\n        if file.endswith(".sub"):\n                cmd = "qsub "+file\n                os.system(cmd)\n'
		python_submit.write(line)
		python_submit.close()
		os.chdir("../../../")
		return

	def Set_MBE_Energy(self):
		for i in range (1, self.mbe_order+1):
			self.mbe_energy[i] = 0.0
			for j in range (1, i+1):
				self.mbe_energy[i] += self.mbe_frags_energy[j]
		return

	def MBE(self,  atom_group=1, cutoff=10, center_atom=0, max_case = 1000000):
		self.Generate_All_MBE_term_General(atom_group, cutoff, center_atom, max_case)
		self.Calculate_All_Frag_Energy_General()
		self.Set_MBE_Energy()
		return

	def Set_Frag_Force_with_Order(self, cm_deri, nn_deri, order):
		self.mbe_frags_deri[order]=np.zeros((self.NAtoms(),3))
		atom_group = self.mbe_frags[order][0].atom_group  # get the number of  atoms per group by looking at the frags.
		for i in range (0, len(self.mbe_frags[order])):
			deri = self.mbe_frags[order][i].Frag_Force(cm_deri[i], nn_deri[i])
			deri = deri.reshape((order, deri.shape[0]/order, -1))
			index_list = self.mbe_frags[order][i].index
			for j in range (0,  len(index_list)):
				self.mbe_frags_deri[order][index_list[j]*atom_group:(index_list[j]+1)*atom_group] += deri[j]
		return

	def Set_MBE_Force(self):
		self.mbe_deri = np.zeros((self.NAtoms(), 3))
		for order in range (1, self.mbe_order+1): # we ignore the 1st order term since we are dealing with helium, debug
			if order in self.mbe_frags_deri.keys():
				self.mbe_deri += self.mbe_frags_deri[order]
		return self.mbe_deri

class Frag(Mol):
	""" Provides a MBE frag of general purpose cluster"""
	def __init__(self, atoms_ =  None, coords_ = None, index_=None, dist_=None, atom_group_=1, frag_type_=None, frag_type_index_=None, FragOrder_=None):
		Mol.__init__(self, atoms_, coords_)
		self.atom_group = atom_group_
		if FragOrder_==None:
			self.FragOrder = self.coords.shape[0]/self.atom_group
		else:
			self.FragOrder = FragOrder_
		if (index_!=None):
			self.index = index_
		else:
			self.index = None
		if (dist_!=None):
			self.dist = dist_
		else:
			self.dist = None
		if (frag_type_!=None):
			self.frag_type = frag_type_
		else:
			self.frag_type = None
		if (frag_type_!=None):
			self.frag_type_index = frag_type_index_
		else:
			self.frag_type_index = None
		self.frag_mbe_energies=dict()
		self.frag_mbe_energy = None
		self.frag_energy = None
		self.permute_index = range (0, self.FragOrder)
		self.permute_sub_index = None
		return

	def PySCF_Frag_MBE_Energy(self,order):   # calculate the MBE of order N of each frag
		"""
		# Below is the old version of PySCF_Frag_MBE_Energy, not working for General MBE, needs to be rewritten, KY

		inner_index = range(0, self.FragOrder)
		real_frag_index=list(itertools.combinations(inner_index,order))
		ghost_frag_index=[]
		for i in range (0, len(real_frag_index)):
			ghost_frag_index.append(list(set(inner_index)-set(real_frag_index[i])))

		i =0
		while(i< len(real_frag_index)):
			#for i in range (0, len(real_frag_index)):
			pyscfatomstring=""
			mol = gto.Mole()
			for j in range (0, order):
				for k in range (0, self.atom_group):
					s = self.coords[real_frag_index[i][j]*self.atom_group+k]
					pyscfatomstring=pyscfatomstring+str(self.AtomName(real_frag_index[i][j]*self.atom_group+k))+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+";"
			for j in range (0, self.FragOrder - order):
				for k in range (0, self.atom_group):
					s = self.coords[ghost_frag_index[i][j]*self.atom_group+k]
					pyscfatomstring=pyscfatomstring+"GHOST"+str(j*self.atom_group+k)+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+";"
			pyscfatomstring=pyscfatomstring[:-1]+"  "
			mol.atom =pyscfatomstring

			mol.basis ={}
			ele_set = list(set(self.AllAtomNames()))
			for ele in ele_set:
				mol.basis[str(ele)]="cc-pvqz"

			for j in range (0, self.FragOrder - order):
				for k in range (0, self.atom_group):
					atom_type = self.AtomName(ghost_frag_index[i][j]*self.atom_group+k)
					mol.basis['GHOST'+str(j*self.atom_group+k)]=gto.basis.load('cc-pvqz',str(atom_type))
			mol.verbose=0
			try:
				print "doing case ", i
				time_log = time.time()
				mol.build()
				mf=scf.RHF(mol)
				hf_en = mf.kernel()
				mp2 = mp.MP2(mf)
				mp2_en = mp2.kernel()
				en = hf_en + mp2_en[0]
				#print "hf_en", hf_en, "mp2_en", mp2_en[0], " en", en
				self.frag_mbe_energies[LtoS(real_frag_index[i])]=en
				print ("pyscf time..", time.time()-time_log)
				i = i+1
				gc.collect()
			except Exception as Ex:
				print "PYSCF Calculation error... :",Ex
				print "Mol.atom:", mol.atom
				print "Pyscf string:", pyscfatomstring
		"""
		raise Exception("Pyscf for General MBE has not be implemented yet")
		return

	def Get_Qchem_Frag_MBE_Energy(self, order, path):
		#print "path:", path, "order:", order
		onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
		#print "onlyfiles:", onlyfiles, "path", path, "order", order
		for outfile_name in onlyfiles:
			if ( outfile_name[-4:]!='.out' ):
					continue
			outfile = open(path+"/"+outfile_name,"r+")
			outfile_lines = outfile.readlines()
			key = None
			rimp2 = None
			for line in outfile_lines:
				if "!" in line:
					key = line[1:-1]
					continue
				if "non-Brillouin singles" in line:
					nonB_single = float(line.split()[3])
					continue
				if "RIMP2         total energy" in line:
					rimp2 = float(line.split()[4])
					continue
				if "fatal error" in line:
					print("fata error! file:", path+"/"+outfile_name)
			if nonB_single != 0.0:
				print("Warning: non-Brillouin singles do not equal to zero, non-Brillouin singles=",nonB_single,path,outfile_name)
			if key!=None and rimp2!=None:
				#print "key:", key, "length:", len(key)
				self.frag_mbe_energies[key] = rimp2
			else:
				print("Qchem Calculation error on ",path,outfile_name)
				raise Exception("Qchem Error")
		return

	def Write_Qchem_Frag_MBE_Input_General(self,order):   # calculate the MBE of order N of each frag
		inner_index = range(0, self.FragOrder)
		real_frag_index=list(itertools.combinations(inner_index,order))
		ghost_frag_index=[]
		for i in range (0, len(real_frag_index)):
			ghost_frag_index.append(list(set(inner_index)-set(real_frag_index[i])))
		i =0
		while(i< len(real_frag_index)):
			charge = 0
			num_ele = 0
			for j in range (0, order):
				charge += self.frag_type[real_frag_index[i][j]]["charge"]
				num_ele += self.frag_type[real_frag_index[i][j]]["num_electron"]
			if num_ele%2 == 0:   # here we always prefer the low spin state
				spin = 1
			else:
				spin = 2
			qchemstring="$molecule\n"+str(charge)+" "+str(spin)+"\n"
			for j in range (0, order):
				pointer = sum(self.atom_group[:real_frag_index[i][j]])
				for k in range (0, self.atom_group[real_frag_index[i][j]]):
					s = self.coords[pointer+k]
					qchemstring+=str(self.AtomName(pointer+k))+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+"\n"
			for j in range (0, self.FragOrder - order):
				pointer = sum(self.atom_group[:ghost_frag_index[i][j]])
				for k in range (0, self.atom_group[ghost_frag_index[i][j]]):
					s = self.coords[pointer+k]
					qchemstring+="@"+str(self.AtomName(pointer+k))+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+"\n"
			qchemstring += "$end\n"
			qchemstring += "!"+LtoS(real_frag_index[i])+"\n"
			qchemstring += Qchem_RIMP2_Block
			qchem_input=open(str(i+1)+".in","w+")
			qchem_input.write(qchemstring)
			qchem_input.close()
			i = i+1
			#gc.collect()  # speed up the function by 1000 times just deleting this single line!
			return


	def Write_Qchem_Frag_MBE_Input_All_General(self, fragnum):
		if not os.path.isdir(str(fragnum)):
			os.mkdir(str(fragnum))
		os.chdir(str(fragnum))
		for i in range (0, self.FragOrder):
			if not os.path.isdir(str(i+1)):
				os.mkdir(str(i+1))
			os.chdir(str(i+1))
			self.Write_Qchem_Frag_MBE_Input_General(i+1)
			os.chdir("..")
		os.chdir("..")
		return

	def Write_Qchem_Frag_MBE_Input_All(self, fragnum):
		if not os.path.isdir(str(fragnum)):
			os.mkdir(str(fragnum))
		os.chdir(str(fragnum))
		for i in range (0, self.FragOrder):
			if not os.path.isdir(str(i+1)):
				os.mkdir(str(i+1))
			os.chdir(str(i+1))
			self.Write_Qchem_Frag_MBE_Input(i+1)
			os.chdir("..")
		os.chdir("..")
		return

	def Get_Qchem_Frag_MBE_Energy_All(self, fragnum, path):
		if not os.path.isdir(path+"/"+str(fragnum)):
			raise Exception(path+"/"+str(fragnum),"is not calculated")
		oldpath = path
		for i in range (0, self.FragOrder):
			path = oldpath+"/"+str(fragnum)+"/"+str(i+1)
			self.Get_Qchem_Frag_MBE_Energy(i+1, path)
		return

	def PySCF_Frag_MBE_Energy_All(self):
		for i in range (0, self.FragOrder):
			self.PySCF_Frag_MBE_Energy(i+1)
		return

	def Set_Frag_MBE_Energy(self):
		self.frag_mbe_energy =  self.Frag_MBE_Energy()
		self.frag_energy = self.frag_mbe_energies[LtoS(self.permute_index)]
		print("self.frag_type: ", self.frag_type)
		print("self.frag_mbe_energy: ", self.frag_mbe_energy)
		return

	def Frag_MBE_Energy(self,  index=None):     # Get MBE energy recursively
		if index==None:
			index=range(0, self.FragOrder)
		order = len(index)
		if order==0:
			return 0
		energy = self.frag_mbe_energies[LtoS(index)]
		for i in range (0, order):
			sub_index = list(itertools.combinations(index, i))
			for j in range (0, len(sub_index)):
				try:
					energy=energy-self.Frag_MBE_Energy( sub_index[j])
				except Exception as Ex:
					print("missing frag energy, error", Ex)
		return  energy

	def CopyTo(self, target):
		target.FragOrder = self.FragOrder
		target.frag_mbe_energies=self.frag_mbe_energies
		target.frag_mbe_energy = self.frag_mbe_energy
		target.frag_energy = self.frag_energy
		target.permute_index = self.permute_index

	def Frag_Force(self, cm_deri, nn_deri):
		return self.Combine_CM_NN_Deri(cm_deri, nn_deri)

	def Combine_CM_NN_Deri(self, cm_deri, nn_deri):
		natom = self.NAtoms()
		frag_deri = np.zeros((natom, 3))
		for i in range (0, natom):  ## debug, this is for not including the diagnol
			for j in range (0, natom):  # debug, this is for not including the diagnol
				if j >= i:
					cm_dx = cm_deri[i][j][0]
					cm_dy = cm_deri[i][j][1]
					cm_dz = cm_deri[i][j][2]
					nn_deri_index = i*(natom+natom-i-1)/2 + (j-i-1) # debug, this is for not including the diagnol
					#nn_deri_index = i*(natom+natom-i+1)/2 + (j-i)  # debug, this is for including the diagnol in the CM
					nn_dcm = nn_deri[nn_deri_index]
				else:
					cm_dx = cm_deri[j][i][3]
					cm_dy = cm_deri[j][i][4]
					cm_dz = cm_deri[j][i][5]
					nn_deri_index = j*(natom+natom-j-1)/2 + (i-j-1)  #debug , this is for not including the diangol
					#nn_deri_index = j*(natom+natom-j+1)/2 + (i-j)    # debug, this is for including the diagnoal in the CM
					nn_dcm = nn_deri[nn_deri_index]
				frag_deri[i][0] += nn_dcm * cm_dx
				frag_deri[i][1] += nn_dcm * cm_dy
				frag_deri[i][2] += nn_dcm * cm_dz
		return frag_deri

class FragableClusterBF(Mol):
	""" All the monomers can pair with each other, no cutoff"""
	def __init__(self, atoms_ =  None, coords_ = None, center_= "COM", cutoff_ = 4.6, width_ = 0.4):
		Mol.__init__(self,atoms_,coords_)
		self.mbe_order = PARAMS["MBE_ORDER"]
		print("MBE order:", self.mbe_order)
		self.center = center_
		self.properties['cutoff'] = cutoff_
		self.properties['cutoff_width'] = width_
		self.frag_list = []    # list of [{"atom":.., "charge":..},{"atom":.., "charge":..},{"atom":.., "charge":..}]
		self.type_of_frags = []  # store the type of frag (1st order) in the self.mbe_frags:  [1,1,1 (H2O), 2,2,2(Na),3,3,3(Cl)]
		self.type_of_frags_dict = {}
		self.atoms_of_frags = [] # store the index of atoms of each frag
		self.mbe_frags=dict()    # list of  frag of each order N, dic['N'=list of frags]
		self.mbe_frags_deri=dict()
		self.type_of_frags_dict = {}
		self.mbe_frags_energy=dict()  # MBE energy of each order N, dic['N'= E_N]
		self.mbe_energy=dict()   # sum of MBE energy up to order N, dic['N'=E_sum]
		self.frag_energy_sum = dict() # sum of the energis of all the frags in certain oder
		self.mbe_force =dict()
		self.nn_force = None
		self.frag_force_sum = dict()
		self.frag_dipole_sum = dict()
		self.mbe_dipole=dict()
		self.nn_dipole = 0
		self.nn_energy = 0.0
		self.frag_charge_sum = dict()
		self.mbe_charge = dict()
		self.nn_charge = None
		return

	def Reset_Frags(self):
		#self.mbe_frags = {}
		self.mbe_frags_deri=dict()
		self.mbe_frags_energy=dict()  # MBE energy of each order N, dic['N'= E_N]
		self.energy=None
		self.mbe_energy=dict()   # sum of MBE energy up to order N, dic['N'=E_sum]
		self.frag_energy_sum = dict()
		self.mbe_deri =None
		self.nn_energy=None
		for order in range (1, self.mbe_order+1):
			for mol_frag in self.mbe_frags[order]:
				#print "old: ", mol_frag.coords
				mol_frag.coords = self.coords[mol_frag.properties["mbe_atom_index"]]
				#print "new:", mol_frag.coords
		#self.mbe_frags = {}
		return


	def Generate_All_MBE_term_General(self, frag_list=[]):
		self.frag_list = frag_list
		for i in range (1, self.mbe_order+1):
			print("Generating order", i)
			self.Generate_MBE_term_General(i)
		return

	def Generate_MBE_term_General(self, order):
		if order in self.mbe_frags.keys():
			return
		if order==1:
			self.mbe_frags[order] = []
			masked=[]
			frag_index = 0
			for i, dic in enumerate(self.frag_list):
				self.type_of_frags_dict[i] = []
				frag_atoms = String_To_Atoms(dic["atom"])
				frag_atoms = [atoi[atom] for atom in frag_atoms]
				num_frag_atoms = len(frag_atoms)
				j = 0
				while (j < self.NAtoms()):
					if j in masked:
						j += 1
					else:
						tmp_list = list(self.atoms[j:j+num_frag_atoms])
					if tmp_list == frag_atoms:
						self.atoms_of_frags.append([])
						masked += range (j, j+num_frag_atoms)
						self.atoms_of_frags[-1]=range (j, j+num_frag_atoms)
						self.type_of_frags.append(i)
						self.type_of_frags_dict[i].append(frag_index)
						tmp_coord = self.coords[j:j+num_frag_atoms,:].copy()
						tmp_atom  = self.atoms[j:j+num_frag_atoms].copy()
						mbe_terms = [frag_index]
						tmp_mol = Mol(tmp_atom, tmp_coord)
						tmp_mol.properties["mbe_atom_index"] = range(j, j+num_frag_atoms)
						if self.center == "Heaviest": # take the first heaviest one
							tmp_mol.properties["center_atom"] = np.where(tmp_mol.atoms == max(tmp_mol.atoms))[0][0]
							tmp_mol.properties["center"] = tmp_mol.coords[np.where(tmp_mol.atoms == max(tmp_mol.atoms))[0][0]]
						elif self.center == "COM":
							tmp_mol.properties["center"] = tmp_mol.Center("Mass")
						elif self.center == "COP":
							tmp_mol.properties["center"] = tmp_mol.Center("Atom")
						else:
							print("This type of center is not implemented yet, set to COM as center")
							tmp_mol.properties["center"] = tmp_mol.Center("Mass")
						self.mbe_frags[order].append(tmp_mol)
						j += num_frag_atoms
						frag_index += 1
						#print self.atoms_of_frags, tmp_list, self.type_of_frags
						#print self.mbe_frags[order][-1].atoms, self.mbe_frags[order][-1].coords
					else:
						j += 1
		else:
			self.mbe_frags[order] = []
			mbe_terms=[]
			time_log = time.time()
			time_now=time.time()
			frag_case = 0
			sample_index = range(len(self.mbe_frags[1]))
			tmp_time  = time.time()
			sub_combinations = list(itertools.combinations(sample_index, order))
			for i in range (0, len(sub_combinations)):
				term = list(sub_combinations[i])
				if len(list(set(term))) < len(term):
					continue
				mbe_terms.append(term)
				frag_case  += 1
			for i in range (0, len(mbe_terms)):
				atom_group = []
				for index in mbe_terms[i]:
					atom_group.append(self.mbe_frags[1][index].atoms.shape[0])
				tmp_coord = np.zeros((sum(atom_group), 3))
				tmp_atom = np.zeros(sum(atom_group), dtype=np.uint8)
				pointer = 0
				mbe_atom_index = []
				frag_mono_center = []
				natom_each_mono = []
				for j, index in enumerate(mbe_terms[i]):
					tmp_coord[pointer:pointer+atom_group[j],:] = self.mbe_frags[1][index].coords
					tmp_atom[pointer:pointer+atom_group[j]] = self.mbe_frags[1][index].atoms
					mbe_atom_index += self.mbe_frags[1][index].properties["mbe_atom_index"]
					natom_each_mono.append(len(self.mbe_frags[1][index].properties["mbe_atom_index"]))
					frag_mono_center.append(self.mbe_frags[1][index].properties["center"])
					pointer += atom_group[j]
				tmp_mol = Mol(tmp_atom, tmp_coord)
				tmp_mol.properties["mbe_atom_index"] = mbe_atom_index
				tmp_mol.properties["mono_index"] = mbe_terms[i]
				tmp_mol.properties["natom_each_mono"] = natom_each_mono
				tmp_mol.properties["center"] = frag_mono_center
				#print "tmp_coords: ", tmp_mol.coords
				self.mbe_frags[order].append(tmp_mol)
			del sub_combinations
		return

	def MBE_Energy(self):
		mono_num = len(self.mbe_frags[1])
		self.nn_energy = 0.0
		for order in range (1, self.mbe_order+1):
			self.mbe_energy[order] = self.frag_energy_sum[order]
			if order == 1:
				self.nn_energy += self.mbe_energy[order]
				continue
			for sub_order in range (1, order):
				self.mbe_energy[order] -= nCr(mono_num-sub_order, order-sub_order)*self.mbe_energy[sub_order]
			print("order: ", order, self.mbe_energy[order])
			self.nn_energy += self.mbe_energy[order]
		print(self.mbe_energy, self.nn_energy)
		return

	def MBE_Energy_Embed(self):
		self.properties["mbe_energy_embed"] = dict()
		mono_num = len(self.mbe_frags[1])
		self.nn_energy = 0.0
		for order in range (1, self.mbe_order+1):
			self.mbe_energy[order] = self.frag_energy_sum[order]
			self.properties["mbe_energy_embed"][order] = self.mbe_energy[order]
			if order == 1:
				self.nn_energy += self.properties["mbe_energy_embed"][order]
				continue
			if order == 2:
				t = time.time()
				self.properties["mbe_energy_embed"][order] = 0.0
				self.mbe_energy[order] = 0.0
				cc_2b_sum = 0.0
				nn_2b_sum = 0.0
				avg_2b_sum = 0.0
				#replu_2b_sum = 0.0
				for mol_frag in self.mbe_frags[order]:
					mol_frag.DistMatrix = MolEmb.Make_DistMat(mol_frag.coords)  # update the distance matrix
					dist =  (sum(np.square(mol_frag.properties["center"][0] - mol_frag.properties["center"][1])))**0.5
					nn_2b = mol_frag.properties["nn_energy"] - self.mbe_frags[1][mol_frag.properties["mono_index"][0]].properties["nn_energy"] -  self.mbe_frags[1][mol_frag.properties["mono_index"][1]].properties["nn_energy"]
					cc_2b = Dimer_ChargeCharge(mol_frag)
					#replu_2b = Dimer_Replusive(mol_frag)
					avg_2b = (1.0-math.tanh((dist - self.properties["cutoff"])/self.properties["cutoff_width"]))/2.0*nn_2b + (1.0+math.tanh((dist - self.properties["cutoff"])/self.properties["cutoff_width"]))/2.0*cc_2b
					#avg_2b = (1.0-math.tanh((dist - self.properties["cutoff"])/self.properties["cutoff_width"]))/2.0*nn_2b + (1.0+math.tanh((dist - self.properties["cutoff"])/self.properties["cutoff_width"]))/2.0*cc_2b + replu_2b
					self.mbe_energy[order] += nn_2b
					mol_frag.properties["nn_2b"] = nn_2b
					mol_frag.properties["cc_2b"] = cc_2b
					self.properties["mbe_energy_embed"][order] += avg_2b
					cc_2b_sum += cc_2b
					nn_2b_sum += nn_2b
					avg_2b_sum  += avg_2b
					#replu_2b_sum  += replu_2b
				self.nn_energy += self.properties["mbe_energy_embed"][order]
				#print "order 2 energy cost:", time.time() -t
				continue
			for sub_order in range (1, order):
				self.mbe_energy[order] -= nCr(mono_num-sub_order, order-sub_order)*self.mbe_energy[sub_order]
			self.properties["mbe_energy_embed"][order]  = self.mbe_energy[order]
			self.nn_energy += self.properties["mbe_energy_embed"][order]
		print(self.properties["mbe_energy_embed"], self.nn_energy)
		return

	def MBE_Dipole(self):
		mono_num = len(self.mbe_frags[1])
		self.nn_dipole = 0.0
		for order in range (1, self.mbe_order+1):
			self.mbe_dipole[order] = self.frag_dipole_sum[order]
			if order == 1:
				self.nn_dipole += self.mbe_dipole[order]
				continue
			for sub_order in range (1, order):
				self.mbe_dipole[order] -= nCr(mono_num-sub_order, order-sub_order)*self.mbe_dipole[sub_order]
			self.nn_dipole += self.mbe_dipole[order]
		print(self.mbe_dipole, self.nn_dipole)
		return

	def MBE_Force(self):
		mono_num = len(self.mbe_frags[1])
		self.nn_force = np.zeros((self.NAtoms(), 3))
		for order in range (1, self.mbe_order+1):
			self.mbe_force[order] = self.frag_force_sum[order]
			if order == 1:
				self.nn_force += self.mbe_force[order]
				continue
			for sub_order in range (1, order):
				self.mbe_force[order] -= nCr(mono_num-sub_order, order-sub_order)*self.mbe_force[sub_order]
			self.nn_force += self.mbe_force[order]
		self.properties["mbe_deri"] = -self.nn_force/JOULEPERHARTREE
		#print self.mbe_force, self.nn_force
		return

	def MBE_Force_Embed(self):
		self.properties["mbe_energy_embed_force"] = dict()
		mono_num = len(self.mbe_frags[1])
		self.nn_force = np.zeros((self.NAtoms(), 3))
		for order in range (1, self.mbe_order+1):
			self.mbe_force[order] = self.frag_force_sum[order]
			if order == 1:
				self.properties["mbe_energy_embed_force"][order] = self.mbe_force[order]
				self.nn_force += self.properties["mbe_energy_embed_force"][order]
				continue
			if order == 2:
				t = time.time()
				cc_2b_grad_sum = np.zeros((self.NAtoms(), 3))
				nn_2b_grad_sum = np.zeros((self.NAtoms(), 3))
				avg_2b_grad_sum = np.zeros((self.NAtoms(), 3))
				#replu_2b_grad_sum = np.zeros((self.NAtoms(), 3))
				for mol_frag in self.mbe_frags[order]:
					dist =  (sum(np.square(mol_frag.properties["center"][0] - mol_frag.properties["center"][1])))**0.5
					A = math.tanh((dist - self.properties["cutoff"])/self.properties["cutoff_width"])/2.0
					cc_2b_grad = np.zeros((self.NAtoms(), 3))
					nn_2b_grad = np.zeros((self.NAtoms(), 3))
					avg_2b_grad = np.zeros((self.NAtoms(), 3))
					cutoff_2b_grad = np.zeros((self.NAtoms(), 3))
					#replu_2b_grad = np.zeros((self.NAtoms(), 3))
					cutoff_2b_grad[mol_frag.properties["mbe_atom_index"]] = Dimer_Cutoff_Grad(mol_frag, dist, self.properties["cutoff"], self.properties["cutoff_width"])
					#replu_2b_grad[mol_frag.properties["mbe_atom_index"]] = Dimer_Replusive_Grad(mol_frag)
					cc_2b_grad[mol_frag.properties["mbe_atom_index"]] = Dimer_ChargeCharge_Grad(mol_frag)
					mono_1_grads = self.mbe_frags[1][mol_frag.properties["mono_index"][0]].properties["nn_energy_grads"]
					mono_2_grads = self.mbe_frags[1][mol_frag.properties["mono_index"][1]].properties["nn_energy_grads"]
					nn_2b_grad[mol_frag.properties["mbe_atom_index"]] = -(mol_frag.properties["nn_energy_grads"] - np.lib.pad(mono_1_grads,((0, mol_frag.properties["natom_each_mono"][1]),(0,0)),'constant', constant_values = (0)) - np.lib.pad(mono_2_grads,((mol_frag.properties["natom_each_mono"][0], 0),(0,0)),'constant', constant_values = (0)))/JOULEPERHARTREE
					avg_2b_grad = (0.5 - A)*nn_2b_grad - cutoff_2b_grad*mol_frag.properties["nn_2b"] + (0.5 + A)*cc_2b_grad + cutoff_2b_grad*mol_frag.properties["cc_2b"]
					#avg_2b_grad = (0.5 - A)*nn_2b_grad - cutoff_2b_grad*mol_frag.properties["nn_2b"] + (0.5 + A)*cc_2b_grad + cutoff_2b_grad*mol_frag.properties["cc_2b"]+replu_2b_grad
					nn_2b_grad_sum += nn_2b_grad
					cc_2b_grad_sum += cc_2b_grad
					avg_2b_grad_sum += avg_2b_grad
					#replu_2b_grad_sum += replu_2b_grad
				self.mbe_force[order] = -nn_2b_grad_sum * JOULEPERHARTREE
				self.properties["mbe_energy_embed_force"][order] = -avg_2b_grad_sum*JOULEPERHARTREE
				self.nn_force +=  self.properties["mbe_energy_embed_force"][order]
				continue
			for sub_order in range (1, order):
				self.mbe_force[order] -= nCr(mono_num-sub_order, order-sub_order)*self.mbe_force[sub_order]
			self.properties["mbe_energy_embed_force"][order] = self.mbe_force[order]
			self.nn_force += self.properties["mbe_energy_embed_force"][order]
			self.properties["mbe_deri"] = -self.nn_force/JOULEPERHARTREE
		return

	def MBE_Charge(self):
		mono_num = len(self.mbe_frags[1])
		self.nn_charge = np.zeros(self.NAtoms())
		for order in range (1, self.mbe_order+1):
			self.mbe_charge[order] = self.frag_charge_sum[order]
			if order == 1:
				self.nn_charge += self.mbe_charge[order]
				continue
			for sub_order in range (1, order):
				self.mbe_charge[order] -= nCr(mono_num-sub_order, order-sub_order)*self.mbe_charge[sub_order]
			self.nn_charge += self.mbe_charge[order]
			#if order == PARAMS["Embedded_Charge_Order"]:
			#	self.properties['embedded_charge'] = np.copy(self.nn_charge)
		#print self.nn_charge, " sum:", np.sum(self.nn_charge)
		return
