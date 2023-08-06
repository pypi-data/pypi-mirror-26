"""
Linear Scaling Atom Neighbor List Generators.
see also: http://scipy-cookbook.readthedocs.io/items/KDTree_example.html
Depending on cutoffs and density these scale to >20,000 atoms

TODO:
	fix bug with generation when there's no neighbors...  IE:
		File "/Users/johnparkhill/TensorMol/TensorMol/TFMolManage.py", line 1288, in EvalBPDirectEEUpdateSinglePeriodic
		rad_p_ele, ang_t_elep, mil_j, mil_jk = NL.buildPairsAndTriplesWithEleIndexPeriodic(Rr_cut, Ra_cut, self.Instances.eles_np, self.Instances.eles_pairs_np)
		File "/Users/johnparkhill/TensorMol/TensorMol/Neighbors.py", line 413, in buildPairsAndTriplesWithEleIndexPeriodic
		trpE_sorted, trtE_sorted, mil_jk, jk_max = self.buildPairsAndTriplesWithEleIndex(rcut_pairs, rcut_triples, ele, elep)
		File "/Users/johnparkhill/TensorMol/TensorMol/Neighbors.py", line 367, in buildPairsAndTriplesWithEleIndex
		prev_l = trtE_sorted[0][4]
"""

from __future__ import absolute_import
from __future__ import print_function
import numpy as np
#from PairProviderTF import *
from .Util import *
from MolEmb import Make_NListNaive, Make_NListLinear
import time

class NeighborList:
	"""
	TODO: incremental tree and neighborlist updates.
	"""
	@TMTiming("NeighborList::init")
	def __init__(self, x_, DoTriples_ = False, DoPerms_ = False, ele_ = None, alg_ = None, sort_ = False):
		"""
		Builds or updates a neighbor list of atoms within rcut_
		using n*Log(n) kd-tree.

		Args:
			x_: coordinate array
			rcut_: distance cutoff.
			ele_: element types of each atoms.
			sort_: whether sorting the jk in triples by atom index
		"""
		self.natom = x_.shape[0] # includes periodic images.
		self.x = x_.T.copy()
		self.pairs = None
		self.triples = None
		self.DoTriples = DoTriples_
		self.DoPerms = DoPerms_
		self.ele = ele_
		self.npairs = None
		self.ntriples = None
		self.alg = 0 if self.natom < 2000000 else 1
		#self.alg = 0 if self.natom < 20000 else 1
		if (alg_ != None):
			self.alg = alg_
		self.sort = sort_
		return

	def Update(self, x_, rcut_pairs=5.0, rcut_triples=5.0, molind_ = None, nreal_ = None):
		"""
		In the future this should only force incremental builds.

		Args:
			x_: coordinates.
			rcut_: cutoff of the force.
			molind_: possible molecule index if we are doing a set.
			nreal_: only generate pairs for the first nreal_ atoms.
		"""
		self.x = x_.copy()
		if (self.DoTriples):
			self.pairs, self.triples = self.buildPairsAndTriples(rcut_pairs,rcut_triples, molind_, nreal_=nreal_)
			self.npairs = self.pairs.shape[0]
			self.ntriples = self.triples.shape[0]
		else:
			self.pairs = self.buildPairs(rcut_pairs, molind_, nreal_=nreal_)
			self.npairs = self.pairs.shape[0]
		return

	@TMTiming("NeighborList::BuildPairs")
	def buildPairs(self, rcut=5.0, molind_=None, nreal_=None):
		"""
		Returns the nonzero pairs, triples in self.x within the cutoff.
		Triples are non-repeating ie: no 1,2,2 or 2,2,2 etc. but unordered

		Args:
			rcut: the cutoff for pairs and triples
		Returns:
			pair matrix (npair X 2)
			triples matrix (ntrip X 3)
		"""
		pair = []
		ntodo = self.natom
		if (nreal_ != None):
			ntodo = int(nreal_)
		pair = None
		if (self.alg==0):
			pair = Make_NListNaive(self.x,rcut,ntodo,int(self.DoPerms))
		else:
			pair = Make_NListLinear(self.x,rcut,ntodo,int(self.DoPerms))
		npairi = map(len,pair)
		npair = sum(npairi)
		p = None
		if (molind_!=None):
			p=np.zeros((npair,3),dtype = np.uint64)
		else:
			p=np.zeros((npair,2),dtype = np.uint64)
		pp = 0
		for i in range(ntodo):
			for j in pair[i]:
				if (molind_!=None):
					p[pp,0]=molind_
					p[pp,1]=i
					p[pp,2]=j
				else:
					p[pp,0]=i
					p[pp,1]=j
				pp = pp+1
		del pair
		return p

	def buildPairsAndTriples(self, rcut_pairs=5.0, rcut_triples=5.0, molind_=None, nreal_=None):
		"""
		Returns the nonzero pairs, triples in self.x within the cutoff.
		Triples are non-repeating ie: no 1,2,2 or 2,2,2 etc. but unordered

		Args:
			rcut: the cutoff for pairs and triples
		Returns:
			pair matrix (npair X 2)
			triples matrix (ntrip X 3)
		"""
		if (self.ele is None):
			print("WARNING... need self.ele for angular SymFunc triples... ")
		pair = []
		tpair = [] # since these may have different cutoff
		ntodo = self.natom
		if (nreal_ != None):
			ntodo = int(nreal_)
		pair = None
		tpair = None

		if (self.alg==0):
			pair = Make_NListNaive(self.x,rcut_pairs,int(ntodo),int(self.DoPerms))
			tpair = Make_NListNaive(self.x,rcut_triples,int(ntodo),int(self.DoPerms))
		else:
			pair = Make_NListLinear(self.x,rcut_pairs,int(ntodo),int(self.DoPerms))
			tpair = Make_NListLinear(self.x,rcut_triples,int(ntodo),int(self.DoPerms))
		npairi = map(len,pair)
		npair = sum(npairi)
		npairi = map(len,tpair)
		#ntrip = sum(map(lambda x: x*x if x>0 else 0, npairi))
		ntrip = sum(map(lambda x: x*(x-1)/2 if x>0 else 0, npairi))
		#print ("npair:", npair, " ntrip:", ntrip, " rcut_triples:", rcut_triples, " tpair", tpair, " ntodo:", int(ntodo), " self.DoPerms", int(self.DoPerms), " x:", self.x[:int(ntodo)], " pair:", pair)
		p = None
		t = None
		if (molind_!=None):
			p=np.zeros((npair,3),dtype = np.uint64)
			t=np.zeros((ntrip,4),dtype = np.uint64)
		else:
			p=np.zeros((npair,2),dtype = np.uint64)
			t=np.zeros((ntrip,3),dtype = np.uint64)
		pp = 0
		tp = 0
		for i in range(ntodo):
			for j in pair[i]:
				if (molind_!=None):
					p[pp,0]=molind_
					p[pp,1]=i
					p[pp,2]=j
				else:
					p[pp,0]=i
					p[pp,1]=j
				pp = pp+1
			for j in tpair[i]:
				for k in tpair[i]:
					#if True:
					if (k > j): # do not do ijk, ikj permutation
					#if (k!=j):
						if (molind_!=None):
							t[tp,0]=molind_
							t[tp,1]=i
							if self.ele is not None and self.ele[j] > self.ele[k]:  # atom will smaller element index alway go first
								t[tp,2]=k
								t[tp,3]=j
							elif self.sort and j > k:
								t[tp,2]=k
								t[tp,3]=j
							else:
								t[tp,2]=j
								t[tp,3]=k
						else:
							t[tp,0]=i
							if self.ele is not None and self.ele[j] > self.ele[k]:
								t[tp,1]=k
								t[tp,2]=j
							elif self.sort and j > k:
								t[tp,1]=k
								t[tp,2]=j
							else:
								t[tp,1]=j
								t[tp,2]=k
						tp=tp+1
		del pair
		del tpair
		return p,t

class NeighborListSet:
	def __init__(self, x_, nnz_, DoTriples_=False, DoPerms_=False, ele_=None, alg_ = None, sort_ = False):
		"""
		A neighborlist for a set

		Args:
			x_: NMol X MaxNAtom X 3 tensor of coordinates.
			nnz_: NMol vector of maximum atoms in each mol.
			ele_: element type of each atom.
			sort_: whether sort jk in triples by atom index
		"""
		self.nlist = []
		self.nmol = x_.shape[0]
		self.maxnatom = x_.shape[1]
		self.alg = 0 if self.maxnatom < 2000000 else 1
		#self.alg = 0 if self.maxnatom < 20000 else 1
		if (alg_ != None):
			self.alg = alg_
		# alg=0 naive quadratic.
		# alg=1 linear scaling
		# alg=2 PairProvider
		self.x = x_.copy()
		self.nnz = nnz_.copy()
		self.nreal = nnz_.copy() # Over-ridden in the WithImages child of this class.
		self.ele = ele_
		self.sort = sort_
		self.pairs = None
		self.DoTriples = DoTriples_
		self.DoPerms = DoPerms_
		self.triples = None
		self.UpdateInterval = 1
		self.UpdateCounter = 0
		self.PairMaker=None
		if (self.alg<2):
			if self.ele is None:
				for i in range(self.nmol):
					self.nlist.append(NeighborList(x_[i,:nnz_[i]],DoTriples_,DoPerms_, None, self.alg, self.sort))
			else:
				for i in range(self.nmol):
					self.nlist.append(NeighborList(x_[i,:nnz_[i]],DoTriples_,DoPerms_, self.ele[i,:nnz_[i]], self.alg, self.sort))
		else:
			raise Exception("Using fucked up old code.")
			self.PairMaker = PairProvider(self.nmol,self.maxnatom)
		return

	@TMTiming("NLSetUpdate")
	def Update(self, x_, rcut_pairs = 5.0, rcut_triples = 5.0):
		if (self.UpdateCounter == 0):
			self.UpdateCounter = self.UpdateCounter + 1
			self.x = x_.copy()
			if (self.DoTriples):
				self.pairs, self.triples = self.buildPairsAndTriples(rcut_pairs,rcut_triples)
			else:
				self.pairs = self.buildPairs(rcut_pairs)
		elif (self.UpdateCounter < self.UpdateInterval):
			self.UpdateCounter = self.UpdateCounter + 1
		else:
			self.UpdateCounter = 0

	def buildPairs(self, rcut=5.0):
		"""
		builds nonzero pairs and triples for current x.

		Args:
			rcut_: a cutoff parameter.
		Returns:
			(nnzero pairs X 3 pair tensor) (mol , I , J)
		"""
		if self.alg < 2:
			for i,mol in enumerate(self.nlist):
				mol.Update(self.x[i,:self.nnz[i]],rcut,rcut,i, self.nreal[i])
		else:
			return self.PairMaker(self.x,rcut,self.nnz)
		nzp = sum([mol.npairs for mol in self.nlist])
		trp = np.zeros((nzp,3),dtype=np.uint64)
		pp = 0
		for mol in self.nlist:
			trp[pp:pp+mol.npairs] = mol.pairs
			pp += mol.npairs
		return trp

	@TMTiming("SetbuildPairsAndTriples")
	def buildPairsAndTriples(self, rcut_pairs=5.0, rcut_triples=5.0):
		"""
		builds nonzero pairs and triples for current x.

		Args:
			rcut_: a cutoff parameter.
		Returns:
			(nnzero pairs X 3 pair tensor) (mol , I , J)
			(nnzero X 4 triples tensor) (mol , I , J , K)
		"""
		if (self.alg==2):
			trp = self.PairMaker(self.x,rcut_pairs,self.nnz)
			trtmp = self.PairMaker(self.x,rcut_triples,self.nnz)
			hack=[[[] for j in range(self.maxnatom)] for i in range(self.nmol)]
			tore = []
			for p in trtmp:
				(hack[p[0]])[p[1]].append(p[2])
			for i in range(self.nmol):
				for j in range(self.maxnatom):
					for k in hack[i][j]:
						tore.append([i,j,k])
			return trp, np.array(tore)
		else:
			for i,mol in enumerate(self.nlist):
				mol.Update(self.x[i,:self.nnz[i]], rcut_pairs, rcut_triples, i, nreal_=self.nreal[i])
			nzp = sum([mol.npairs for mol in self.nlist])
			nzt = sum([mol.ntriples for mol in self.nlist])
			trp = np.zeros((nzp,3),dtype=np.uint64)
			trt = np.zeros((nzt,4),dtype=np.uint64)
			pp = 0
			tp = 0
			for mol in self.nlist:
				trp[pp:pp+mol.npairs] = mol.pairs
				trt[tp:tp+mol.ntriples] = mol.triples
				pp += mol.npairs
				tp += mol.ntriples
			return trp, trt

	@TMTiming("buildPairsWithBothEleIndex")
	def buildPairsWithBothEleIndex(self, rcut=5.0, ele=None):
		trp  = self.buildPairs(rcut)
		Z1 = self.ele[trp[:, 0], trp[:, 1]]
		Z2 = self.ele[trp[:, 0], trp[:, 2]]
		pair_mask1 = np.equal(Z1.reshape(trp.shape[0],1,1), ele.reshape(ele.shape[0],1))
		pair_mask2 = np.equal(Z2.reshape(trp.shape[0],1,1), ele.reshape(ele.shape[0],1))
		pair_index1 = np.where(np.all(pair_mask1, axis=-1))[1]
		pair_index2 = np.where(np.all(pair_mask2, axis=-1))[1]
		trpE1E2 = np.concatenate((trp, pair_index1.reshape((-1,1)), pair_index2.reshape((-1,1))), axis=-1)
		#print ("trpE1E2:", trpE1E2.shape)
		return trpE1E2

	def buildPairsAndTriplesWithEleIndex(self, rcut_pairs=5.0, rcut_triples=5.0, ele=None, elep=None):
		"""
		generate sorted pairs and triples with index of correspoding ele or elepair append to it.
		sorted order: mol, i (center atom), l (ele or elepair index), j (connected atom 1), k (connected atom 2 for triples)

		Args:
			rcut_: a cutoff parameter.
			ele: element
			elep: element pairs
		Returns:
			(nnzero pairs X 4 pair tensor) (mol, I, J, L)
			(nnzero triples X 5 triple tensor) (mol, I, J, K, L)
		"""

		if not self.sort:
			print ("Warning! Triples need to be sorted")
		# if self.ele == None:
		# 	raise Exception("Element type of each atom is needed.")
		#import time
		t0 = time.time()
		trp, trt = self.buildPairsAndTriples(rcut_pairs, rcut_triples)
		#print ("trp, trt",trp.shape, trt.shape)
		#print ("build P and T time:", time.time()-t0)
		#print ("trp:", trp, "trt:", trt)
		t_start = time.time()
		eleps = np.hstack((elep, np.flip(elep, axis=1))).reshape((elep.shape[0], 2, -1))
		Z = self.ele[trp[:, 0], trp[:, 2]]
		pair_mask = np.equal(Z.reshape(trp.shape[0],1,1), ele.reshape(ele.shape[0],1))
		pair_index = np.where(np.all(pair_mask, axis=-1))[1]
		Z1 = self.ele[trt[:, 0], trt[:, 2]]
		Z2 = self.ele[trt[:, 0], trt[:, 3]]
		Z1Z2 = np.transpose(np.vstack((Z1, Z2)))
		trip_mask = np.equal(Z1Z2.reshape((trt.shape[0],1,1,2)), eleps.reshape((eleps.shape[0],2,2)))
		trip_index = np.where(np.any(np.all(trip_mask, axis=-1),axis=-1))[1]
		trpE = np.concatenate((trp, pair_index.reshape((-1,1))), axis=-1)
		trtE = np.concatenate((trt, trip_index.reshape((-1,1))), axis=-1)
		sort_index = np.lexsort((trpE[:,2], trpE[:,3], trpE[:,1], trpE[:,0]))
		trpE_sorted = trpE[sort_index]
		sort_index = np.lexsort((trtE[:,2], trtE[:,3], trtE[:,4], trtE[:,1], trtE[:,0]))
		trtE_sorted = trtE[sort_index]
		#print ("numpy lexsorting time:", time.time() -t0)
		#print ("time to append and sort element", time.time() - t_start)
		valance_pair = np.zeros(trt.shape[0])
		pointer = 0
		if (len(trtE_sorted)==0):
			mil_jk = np.zeros((trt.shape[0],4))
			jk_max = 0
			return trpE_sorted, trtE_sorted, mil_jk, jk_max
		prev_l = trtE_sorted[0][4]
		prev_atom = trtE_sorted[0][1]
		prev_mol = trtE_sorted[0][0]
		for i in range(0, trt.shape[0]):
			current_l = trtE_sorted[i][4]
			current_atom = trtE_sorted[i][1]
			current_mol = trtE_sorted[i][0]
			#print ("i:       ", i)
			#print ("prev:    ", prev_l)
			#print ("current: ", current_l)
			if current_l == prev_l and current_atom == prev_atom and current_mol == prev_mol:
				pointer += 1
				if i == trt.shape[0]-1:
					valance_pair[i-pointer+1:]=range(0, pointer)
				else:
					pass
			else:
				valance_pair[i-pointer:i]=range(0, pointer)
				pointer = 1
				prev_l = current_l
				prev_atom = current_atom
				prev_mol = current_mol
		#print ("valance_pair:", valance_pair[:20])
		#print ("trtE:", trtE_sorted[:20])
		mil_jk = np.zeros((trt.shape[0],4))
		mil_jk[:,[0,1,2]]= trtE_sorted[:,[0,1,4]]
		mil_jk[:,3] = valance_pair
		#print ("mil_jk", mil_jk)
		jk_max = np.max(valance_pair)
		#print ("after processing time:", time.time() - t_start)
		#print (trpE_sorted, trtE_sorted, jk_max)
		return trpE_sorted, trtE_sorted, mil_jk, jk_max

	@TMTiming("buildPairsAndTriplesWithEleIndexPeriodic")
	def buildPairsAndTriplesWithEleIndexPeriodic(self, rcut_pairs=5.0, rcut_triples=5.0, ele=None, elep=None):
		"""
		generate sorted pairs and triples with index of correspoding ele or elepair append to it.
		sorted order: mol, i (center atom), l (ele or elepair index), j (connected atom 1), k (connected atom 2 for triples)

		Args:
			rcut_: a cutoff parameter.
			ele: element
			elep: element pairs
		Returns:
			(nnzero pairs X 4 pair tensor) (mol, I, J, L)
			(nnzero triples X 5 triple tensor) (mol, I, J, K, L)
		"""
		trpE_sorted, trtE_sorted, mil_jk, jk_max = self.buildPairsAndTriplesWithEleIndex(rcut_pairs, rcut_triples, ele, elep)
		mil_j = np.zeros((trpE_sorted.shape[0], 4))
		pair_pair = np.zeros(trpE_sorted.shape[0])
		if (len(trpE_sorted)==0):
			return trpE_sorted, trtE_sorted, mil_j, mil_jk
		prev_l = trpE_sorted[0][3]
		prev_atom = trpE_sorted[0][1]
		prev_mol = trpE_sorted[0][0]
		pointer = 0
		for i in range(0, trpE_sorted.shape[0]):
			current_l = trpE_sorted[i][3]
			current_atom = trpE_sorted[i][1]
			current_mol = trpE_sorted[i][0]
			if current_l == prev_l and current_atom == prev_atom and current_mol == prev_mol:
				pointer += 1
				if i == trpE_sorted.shape[0]-1:
					pair_pair[i-pointer+1:]=range(0, pointer)
				else:
					pass
			else:
				pair_pair[i-pointer:i]=range(0, pointer)
				pointer = 1
				prev_l = current_l
				prev_atom = current_atom
				prev_mol = current_mol
		mil_j[:,[0,1,2]] = trpE_sorted[:,[0,1,3]]
		mil_j[:,3] = pair_pair
		#print ("trpE_sorted, trtE_sorted",trpE_sorted.shape, trtE_sorted.shape)
		return trpE_sorted, trtE_sorted, mil_j, mil_jk

class NeighborListSetWithImages(NeighborListSet):
	def __init__(self, x_, nnz_, nreal_,  DoTriples_=False, DoPerms_=False, ele_=None, alg_ = None, sort_ = False):
		"""
		A neighborlist for a set which avoids calculating the energy of "image" atoms,
		which are generated only for the periodic components of a force, and
		do not contribute to energy or force.

		Args:
			x_: NMol X MaxNAtom X 3 tensor of coordinates.
			nnz_: NMol vector of maximum atoms in each mol.
			nreal_: NMol vector of real atoms in each mol.
			ele_: element type of each atom.
			sort_: whether sort jk in triples by atom index
		"""
		NeighborListSet.__init__(self, x_,nnz_,DoTriples_,DoPerms_,ele_,alg_ ,sort_)
		self.nreal = nreal_
		return

class CellList:
	"""
	TODO: CellList updates.
	- Determine optimal number of Voxels.
	"""
	def __init__(self, x_, cutoff_ = 5.0, ele_ = None, padding_ = 1.0):
		"""
		Builds or updates a cubic cell list. Each cell size  = 2*cutoff_.
		Args:
			x_: coordinate array
			cutoff_: interaction cutoff
			ele_: element types of each atoms.
			padding_: padding of the molecule box.
		"""
		self.natom = x_.shape[0] # includes periodic images.
		self.x = x_.copy()
		self.ele = ele_
		self.cutoff = cutoff_
		self.Rcore = self.cutoff   # in current implementation, Rcore has to equal Rskin
		self.Rskin = self.cutoff
		self.Rcell = self.Rcore + 2*self.Rskin
		self.padding = padding_
		from itertools import product
		self.offset = np.asarray(list(product([-1, 0, 1], repeat=3)),dtype=int)
		return

	def Update(self, x_):
		self.x = x_.copy()
		core_begin_end = np.array([[np.min(self.x[:,0])-self.padding, np.max(self.x[:,0])+self.padding],\
			[np.min(self.x[:,1])-self.padding, np.max(self.x[:,1])+self.padding],\
			[np.min(self.x[:,2])-self.padding, np.max(self.x[:,2])+self.padding]])
		#print ("core_begin_end:", core_begin_end)
		core_size = core_begin_end[:,1] - core_begin_end[:,0]
		n_core = np.array([core_size[0]/self.Rcore, core_size[1]/self.Rcore, core_size[2]/self.Rcore], dtype=int) + 1
		n_cell = n_core.copy()
		cell_begin_end = core_begin_end + np.array([-self.Rskin, self.Rskin])
		#print ("cell_begin_end:", cell_begin_end)
		#print ("n_core:", n_core)
		core_index = [[] for i in range(0, np.prod(n_core))]
		cell_index = [[] for i in range(0, np.prod(n_cell))]
		for i in range (0, self.natom):
			atom_core_index = ((self.x[i]  - core_begin_end[:,0])/self.Rcore).astype(int)
			core_index[atom_core_index[0]*n_core[1]*n_core[2]+atom_core_index[1]*n_core[2]+atom_core_index[2]].append(i)
			tmp  =  atom_core_index + self.offset
			atom_cell_index = tmp[(tmp[:,0] >= 0) & (tmp[:,0] <  n_cell[0]) & (tmp[:,1] >= 0) & (tmp[:,1] <  n_cell[1]) &  (tmp[:,2] >= 0) & (tmp[:,2] <  n_cell[2])]
			for j in list(atom_cell_index[:,0]*n_cell[1]*n_cell[2]+atom_cell_index[:,1]*n_cell[2]+atom_cell_index[:,2]):
				cell_index[j].append(i)
		#print ("core_index:", core_index)
		#print ("cell_index:", cell_index)
		return core_index, cell_index
