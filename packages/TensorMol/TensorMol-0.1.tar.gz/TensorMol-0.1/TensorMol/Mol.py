from __future__ import absolute_import
from __future__ import print_function
from .Util import *
import MolEmb, TensorMol.Electrostatics
from .LinearOperations import *

class Mol:
	""" Provides a general purpose molecule"""
	def __init__(self, atoms_ =  np.zeros(1,dtype=np.uint8), coords_ = np.zeros(shape=(1,1),dtype=np.float)):
		"""
		Args:
			atoms_: np.array(dtype=uint8) of atomic numbers.
			coords_: np.array(dtype=uint8) of coordinates.
		"""
		self.atoms = atoms_.copy()
		self.coords = coords_.copy()
		self.properties = {}
		self.name=None
		#things below here are sometimes populated if it is useful.
		self.PESSamples = [] # a list of tuples (atom, new coordinates, energy) for storage.
		self.ecoords = None # equilibrium coordinates.
		self.DistMatrix = None # a list of equilbrium distances, for GO-models.
		return

	def ToFragSet(self,frags):
		"""
		Divides this molecule into a set of molecules
		based on fragments

		Args:
			frags: list of integer lists
		Returns:
			An MSet with many mols in it divided by frags.
		"""
		mset = MSet("Fset",PARAMS["sets_dir"],False)
		for frag in frags:
			mset.mols.append(Mol(self.atoms[frags],self.coords[frags]))
		return mset

	def AtomTypes(self):
		return np.unique(self.atoms)

	def Num_of_Heavy_Atom(self):
		return len([1 for i in self.atoms if i!=1])

	def NEles(self):
		return len(self.AtomTypes())

	def IsIsomer(self,other):
		return np.array_equals(np.sort(self.atoms),np.sort(other.atoms))

	def NAtoms(self):
		return self.atoms.shape[0]

	def NumOfAtomsE(self, e):
		return sum( [1 if at==e else 0 for at in self.atoms ] )

	def CalculateAtomization(self):
		if ("roomT_H" in self.properties):
			AE = self.properties["roomT_H"]
			for i in range (0, self.atoms.shape[0]):
				if (self.atoms[i] in ELEHEATFORM):
					AE = AE - ELEHEATFORM[self.atoms[i]]
			self.properties["atomization"] = AE
		elif ("energy" in self.properties):
			AE = self.properties["energy"]
			for i in range (0, self.atoms.shape[0]):
				if (self.atoms[i] in ele_U):
					AE = AE - ele_U[self.atoms[i]]
			self.properties["atomization"] = AE
		else:
			raise Exception("Missing data... ")
		return

	def Calculate_vdw(self):
		c = 0.38088
		self.vdw = 0.0
		s6 = S6['B3LYP']
		self.properties["vdw"] = 0.0
		for i in range (0, self.NAtoms()):
			atom1 = self.atoms[i]
			for j in range (i+1, self.NAtoms()):
				atom2 = self.atoms[j]
				self.properties["vdw"] += -s6*c*((C6_coff[atom1]*C6_coff[atom2])**0.5)/(self.DistMatrix[i][j])**6 * (1.0/(1.0+6.0*(self.DistMatrix[i][j]/(atomic_vdw_radius[atom1]+atomic_vdw_radius[atom2]))**-12))
		return
	def Rotate(self, axis, ang, origin=np.array([0.0, 0.0, 0.0])):
		"""
		Rotate atomic coordinates and forces if present.

		Args:
			axis: vector for rotation axis
			ang: radians of rotation
			origin: origin of rotation axis.
		"""
		rm = RotationMatrix(axis, ang)
		crds = np.copy(self.coords)
		crds -= origin
		for i in range(len(self.coords)):
			self.coords[i] = np.dot(rm,crds[i])
		if ("forces" in self.properties.keys()):
			# Must also rotate the force vectors
			old_endpoints = crds+self.properties["forces"]
			new_forces = np.zeros(crds.shape)
			for i in range(len(self.coords)):
				new_endpoint = np.dot(rm,old_endpoints[i])
				new_forces[i] = new_endpoint - self.coords[i]
			self.properties["forces"] = new_forces
		self.coords += origin
	def RotateRandomUniform(self, randnums=None, origin=np.array([0.0, 0.0, 0.0])):
		"""
		Rotate atomic coordinates and forces if present.

		Args:
			randnums: theta, phi, and z for rotation, if None then rotation is random
			origin: origin of rotation axis.
		"""
		rm = RotationMatrix_v2(randnums)
		crds = np.copy(self.coords)
		crds -= origin
		self.coords = np.einsum("ij,kj->ki",rm, crds)
		if ("forces" in self.properties.keys()):
			# Must also rotate the force vectors
			old_endpoints = crds+self.properties["forces"]
			new_endpoint = np.einsum("ij,kj->ki",rm, old_endpoints)
			new_forces = new_endpoint - self.coords
			self.properties["forces"] = new_forces
		if ("mmff94forces" in self.properties.keys()):
			# Must also rotate the force vectors
			old_endpoints = crds+self.properties["mmff94forces"]
			new_endpoint = np.einsum("ij,kj->ki",rm, old_endpoints)
			new_forces = new_endpoint - self.coords
			self.properties["mmff94forces"] = new_forces
		self.coords += origin
	def Transform(self,ltransf,center=np.array([0.0,0.0,0.0])):
		crds=np.copy(self.coords)
		for i in range(len(self.coords)):
			self.coords[i] = np.dot(ltransf,crds[i]-center) + center
	def AtomsWithin(self,rad, pt):
		# Returns indices of atoms within radius of point.
		dists = map(lambda x: np.linalg.norm(x-pt),self.coords)
		return [i for i in range(self.NAtoms()) if dists[i]<rad]
	def Distort(self,disp=0.38,movechance=.20):
		''' Randomly distort my coords, but save eq. coords first '''
		self.BuildDistanceMatrix()
		e0= self.GoEnergy(self.coords)
		for i in range(0, self.atoms.shape[0]):
			for j in range(0, 3):
				if (random.uniform(0, 1)<movechance):
					#only accept collisionless moves.
					accepted = False
					maxiter = 100
					while (not accepted and maxiter>0):
						tmp = self.coords
						tmp[i,j] += np.random.normal(0.0, disp)
						mindist = np.min([ np.linalg.norm(tmp[i,:]-tmp[k,:]) if i!=k else 1.0 for k in range(self.NAtoms()) ])
						if (mindist>0.35):
							accepted = True
							self.coords = tmp
						maxiter=maxiter-1

	def DistortAN(self,movechance=.15):
		''' Randomly replace atom types. '''
		for i in range(0, self.atoms.shape[0]):
			if (random.uniform(0, 1)<movechance):
				self.atoms[i] = random.random_integers(1,PARAMS["MAX_ATOMIC_NUMBER"])
	def read_xyz_with_properties(self, path, properties, center=True):
		try:
			f=open(path,"r")
			lines=f.readlines()
			natoms=int(lines[0])
			self.atoms.resize((natoms))
			self.coords.resize((natoms,3))
			for i in range(natoms):
				line = lines[i+2].split()
				self.atoms[i]=AtomicNumber(line[0])
				for j in range(3):
					try:
						self.coords[i,j]=float(line[j+1])
					except:
						self.coords[i,j]=scitodeci(line[j+1])
			if center:
				self.coords -= self.Center()
			properties_line = lines[1]
			for i, mol_property in enumerate(properties):
				if mol_property == "name":
					self.properties["name"] = properties_line.split(";")[i]
				if mol_property == "energy":
					self.properties["energy"] = float(properties_line.split(";")[i])
				if mol_property == "forces":
					self.properties['forces'] = np.zeros((natoms, 3))
					read_forces = (properties_line.split(";")[i]).split(",")
					for j in range(natoms):
						for k in range(3):
							self.properties['forces'][j,k] = float(read_forces[j*3+k])
				if mol_property == "dipoles":
					self.properties['dipoles'] = np.zeros((3))
					read_dipoles = (properties_line.split(";")[i]).split(",")
					for j in range(3):
						self.properties['dipoles'][j] = float(read_dipoles[j])
				if mol_property == "mulliken_charges":
					self.properties["mulliken_charges"] = np.zeros((natoms))
					read_charges = (properties_line.split(";")[i]).split(",")
					for j in range(natoms):
						self.properties["mulliken_charges"] = float(read_charges[j])
			f.close()
		except Exception as Ex:
			print("Read Failed.", Ex)
			raise Ex
		return
	def ReadGDB9(self,path,filename):
		try:
			f=open(path,"r")
			lines=f.readlines()
			natoms=int(lines[0])
			self.name = filename[0:-4]
			self.atoms.resize((natoms))
			self.coords.resize((natoms,3))
			try:
				self.properties["energy"] = float((lines[1].split())[12])
				self.properties["roomT_H"] = float((lines[1].split())[14])
			except:
				pass
			for i in range(natoms):
				line = lines[i+2].split()
				self.atoms[i]=AtomicNumber(line[0])
				try:
					self.coords[i,0]=float(line[1])
				except:
					self.coords[i,0]=scitodeci(line[1])
				try:
					self.coords[i,1]=float(line[2])
				except:
					self.coords[i,1]=scitodeci(line[2])
				try:
					self.coords[i,2]=float(line[3])
				except:
					self.coords[i,2]=scitodeci(line[3])
			f.close()
		except Exception as Ex:
			print("Read Failed.", Ex)
			raise Ex
		if (("energy" in self.properties) or ("roomT_H" in self.properties)):
			self.CalculateAtomization()
		return
	def Clean(self):
		self.DistMatrix = None
	def ParseProperties(self,s_):
		"""
		The format of a property string is
		Comment: PropertyName1 Array ;PropertyName2 Array;
		The Property names and contents cannot contain ; :
		"""
		t = s_.split("Comment:")
		t2 = t[1].split(";;;")
		tore = {}
		for prop in t2:
			s = prop.split()
			if (len(s)<1):
				continue
			elif (s[0]=='energy'):
				tore["energy"] = float(s[1])
			elif (s[0]=='Lattice'):
				tore["Lattice"] = np.fromstring(s[1]).reshape((3,3))
		return tore
	def PropertyString(self):
		tore = ""
		for prop in self.properties.keys():
			try:
				if (prop == "energy"):
					tore = tore +";;;"+prop+" "+str(self.properties["energy"])
				elif (prop == "Lattice"):
					tore = tore +";;;"+prop+" "+(self.properties[prop]).tostring()
				else:
					tore = tore +";;;"+prop+" "+str(self.properties[prop])
			except Exception as Ex:
				# print "Problem with energy", string
				pass
		return tore
	def FromXYZString(self,string):
		lines = string.split("\n")
		natoms=int(lines[0])
		if (len(lines[1].split())>1):
			try:
				self.properties = self.ParseProperties(lines[1])
			except Exception as Ex:
				print("Problem with energy", Ex)
				pass
		self.atoms.resize((natoms))
		self.coords.resize((natoms,3))
		for i in range(natoms):
			line = lines[i+2].split()
			if len(line)==0:
				return
			self.atoms[i]=AtomicNumber(line[0])
			try:
				self.coords[i,0]=float(line[1])
			except:
				self.coords[i,0]=scitodeci(line[1])
			try:
				self.coords[i,1]=float(line[2])
			except:
				self.coords[i,1]=scitodeci(line[2])
			try:
				self.coords[i,2]=float(line[3])
			except:
				self.coords[i,2]=scitodeci(line[3])
		if ("energy" in self.properties):
			self.CalculateAtomization()
		return
	def __str__(self,wprop=False):
		lines =""
		natom = self.atoms.shape[0]
		if (wprop):
			lines = lines+(str(natom)+"\nComment: "+self.PropertyString()+"\n")
		else:
			lines = lines+(str(natom)+"\nComment: \n")
		for i in range (0, natom):
			atom_name =  atoi.keys()[atoi.values().index(self.atoms[i])]
			lines = lines+(atom_name+"   "+str(self.coords[i][0])+ "  "+str(self.coords[i][1])+ "  "+str(self.coords[i][2])+"\n")
		return lines
	def __repr__(self):
		return self.__str__()
	def WriteXYZfile(self, fpath=".", fname="mol", mode="a", wprop = False):
		if not os.path.exists(os.path.dirname(fpath+"/"+fname+".xyz")):
			try:
				os.makedirs(os.path.dirname(fpath+"/"+fname+".xyz"))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		with open(fpath+"/"+fname+".xyz", mode) as f:
			for line in self.__str__(wprop).split("\n"):
				f.write(line+"\n")
	def WriteSmiles(self, fpath=".", fname="gdb9_smiles", mode = "a"):
		if not os.path.exists(os.path.dirname(fpath+"/"+fname+".dat")):
			try:
				os.makedirs(os.path.dirname(fpath+"/"+fname+".dat"))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		with open(fpath+"/"+fname+".dat", mode) as f:
			f.write(self.name+ "  "+ self.smiles+"\n")
			f.close()
		return
	def XYZtoGridIndex(self, xyz, ngrids = 250,padding = 2.0):
		Max = (self.coords).max() + padding
		Min = (self.coords).min() - padding
		binsize = (Max-Min)/float(ngrids-1)
		x_index = math.floor((xyz[0]-Min)/binsize)
		y_index = math.floor((xyz[1]-Min)/binsize)
		z_index = math.floor((xyz[2]-Min)/binsize)
		#index=int(x_index+y_index*ngrids+z_index*ngrids*ngrids)
		return x_index, y_index, z_index

	def MolDots(self, ngrids = 250 , padding =2.0, width = 2):
		grids = self.MolGrids()
		for i in range (0, self.atoms.shape[0]):
			x_index, y_index, z_index = self.XYZtoGridIndex(self.coords[i])
			for m in range (-width, width):
				for n in range (-width, width):
					for k in range (-width, width):
						index = (x_index)+m + (y_index+n)*ngrids + (z_index+k)*ngrids*ngrids
						grids[index] = atoc[self.atoms[i]]
		return grids

	def Center(self, CenterOf="Atom", MomentOrder = 1.):
		''' Returns the center of atom or mass

		Args:
			CenterOf: Whether to return center of atom position or mass.
			MomentOrder: Option to do nth order moment.
		Returns:
			Center of Atom, Mass, or a higher-order moment.
		'''
		if (CenterOf == "Mass"):
			m = np.array(map(lambda x: ATOMICMASSES[x-1],self.atoms))
			return np.einsum("ax,a->x",np.power(self.coords,MomentOrder),m)/np.sum(m)
		else:
			return np.average(np.power(self.coords,MomentOrder),axis=0)

	def rms(self, m):
		""" Cartesian coordinate difference. """
		err  = 0.0
		for i in range (0, (self.coords).shape[0]):
			err += np.linalg.norm(m.coords[i] - self.coords[i])
		return err/self.coords.shape[0]

	def rms_inv(self, m):
		""" Invariant coordinate difference. """
		mdm = MolEmb.Make_DistMat(self.coords)
		odm = MolEmb.Make_DistMat(m.coords)
		tmp = (mdm-odm)
		return np.sqrt(np.sum(tmp*tmp)/(mdm.shape[0]*mdm.shape[0]))

	def MolGrids(self, ngrids = 250):
		grids = np.zeros((ngrids, ngrids, ngrids), dtype=np.uint8)
		grids = grids.reshape(ngrids**3)   #kind of ugly, but lets keep it for now
		return grids

	def SpanningGrid(self,num=250,pad=4.,Flatten=True, Cubic = True):
		''' Returns a regular grid the molecule fits into '''
		xmin=np.min(self.coords[:,0])-pad
		xmax=np.max(self.coords[:,0])+pad
		ymin=np.min(self.coords[:,1])-pad
		ymax=np.max(self.coords[:,1])+pad
		zmin=np.min(self.coords[:,2])-pad
		zmax=np.max(self.coords[:,2])+pad
		lx = xmax-xmin
		ly = ymax-ymin
		lz = zmax-zmin
		if (Cubic):
			mlen = np.max([lx,ly,lz])
			xmax = xmin + mlen
			ymax = ymin + mlen
			zmax = zmin + mlen
		grids = np.mgrid[xmin:xmax:num*1j, ymin:ymax:num*1j, zmin:zmax:num*1j]
		grids = grids.transpose((1,2,3,0))
		if (not Flatten):
			return grids.rshape()
		grids = grids.reshape((grids.shape[0]*grids.shape[1]*grids.shape[2], grids.shape[3]))
		return grids, (xmax-xmin)*(ymax-ymin)*(zmax-zmin)

	def AddPointstoMolDots(self, grids, points, value, ngrids =250):  # points: x,y,z,prob    prob is in (0,1)
		points = points.reshape((-1,3))  # flat it
		value = value.reshape(points.shape[0]) # flat it
		value = value/value.max()
		for i in range (0, points.shape[0]):
			x_index, y_index, z_index = self.XYZtoGridIndex(points[i])
			index = x_index + y_index*ngrids + z_index*ngrids*ngrids
			if grids[index] <  int(value[i]*250):
				grids[index] = int(value[i]*250)
		return grids

	def SortAtoms(self):
		""" First sorts by element, then sorts by distance to the center of the molecule
			This improves alignment. """
		order = np.argsort(self.atoms)
		self.atoms = self.atoms[order]
		self.coords = self.coords[order,:]
		self.coords = self.coords - self.Center()
		self.ElementBounds = [[0,0] for i in range(self.NEles())]
		for e, ele in enumerate(self.AtomTypes()):
			inblock=False
			for i in range(0, self.NAtoms()):
				if (not inblock and self.atoms[i]==ele):
					self.ElementBounds[e][0] = i
					inblock=True
				elif (inblock and (self.atoms[i]!=ele or i==self.NAtoms()-1)):
					self.ElementBounds[e][1] = i
					inblock=False
					break
		for e in range(self.NEles()):
			blk = self.coords[self.ElementBounds[e][0]:self.ElementBounds[e][1],:].copy()
			dists = np.sqrt(np.sum(blk*blk,axis=1))
			inds = np.argsort(dists)
			self.coords[self.ElementBounds[e][0]:self.ElementBounds[e][1],:] = blk[inds]
		return

	def WriteInterpolation(self,b,n=10):
		for i in range(n): # Check the interpolation.
			m=Mol(self.atoms,self.coords*((9.-i)/9.)+b.coords*((i)/9.))
			m.WriteXYZfile(PARAMS["results_dir"], "Interp"+str(n))

	def AlignAtoms(self, m):
		"""
		Align the geometries and atom order of myself and another molecule.
		This alters both molecules, centering them, and also permutes
		their atoms.

		Args:
			m: A molecule to be aligned with me.
		"""
		assert self.NAtoms() == m.NAtoms(), "Number of atoms do not match"
		self.coords -= self.Center()
		m.coords -= m.Center()
		# try to achieve best rotation alignment between them by aligning the second moments of position
		sdm = MolEmb.Make_DistMat(self.coords)
		d = sdm-MolEmb.Make_DistMat(m.coords)
		BestMomentOverlap = np.sum(d*d)
		BestTriple=[0.,0.,0.]
		for a in np.linspace(-Pi,Pi,20):
			for b in np.linspace(-Pi,Pi,20):
				for c in np.linspace(-Pi,Pi,20):
					tmpm = Mol(m.atoms,m.coords)
					tmpm.Rotate([1.,0.,0.],a)
					tmpm.Rotate([0.,1.,0.],b)
					tmpm.Rotate([0.,0.,1.],c)
					d = sdm-MolEmb.Make_DistMat(tmpm.coords)
					lap = np.sum(d*d)
					if ( lap < BestMomentOverlap ):
						BestTriple = [a,b,c]
						BestMomentOverlap = lap
		m.Rotate([1.,0.,0.],BestTriple[0])
		m.Rotate([0.,1.,0.],BestTriple[1])
		m.Rotate([0.,0.,1.],BestTriple[2])
		#print("After centering and Rotation ---- ")
		#print("Self \n"+self.__str__())
		#print("Other \n"+m.__str__())
		self.SortAtoms()
		m.SortAtoms()
		# Greedy assignment
		for e in range(self.NEles()):
			mones = range(self.ElementBounds[e][0],self.ElementBounds[e][1])
			mtwos = range(self.ElementBounds[e][0],self.ElementBounds[e][1])
			assignedmones=[]
			assignedmtwos=[]
			for b in mtwos:
				acs = self.coords[mones]
				tmp = acs - m.coords[b]
				best = np.argsort(np.sqrt(np.sum(tmp*tmp,axis=1)))[0]
				#print "Matching ", m.coords[b]," to ", self.coords[mones[best]]
				#print "Matching ", b," to ", mones[best]
				assignedmtwos.append(b)
				assignedmones.append(mones[best])
				mones = complement(mones,assignedmones)
			self.coords[mtwos] = self.coords[assignedmones]
			m.coords[mtwos] = m.coords[assignedmtwos]
		self.DistMatrix = MolEmb.Make_DistMat(self.coords)
		m.DistMatrix = MolEmb.Make_DistMat(m.coords)
		diff = np.linalg.norm(self.DistMatrix - m.DistMatrix)
		tmp_coords=m.coords.copy()
		tmp_dm = MolEmb.Make_DistMat(tmp_coords)
		k = 0
		steps = 1
		while (k < 2):
			for i in range(m.NAtoms()):
				for j in range(i+1,m.NAtoms()):
					if m.atoms[i] != m.atoms[j]:
						continue
					ir = tmp_dm[i].copy() - self.DistMatrix[i]
					jr = tmp_dm[j].copy() - self.DistMatrix[j]
					irp = tmp_dm[j].copy()
					irp[i], irp[j] = irp[j], irp[i]
					jrp = tmp_dm[i].copy()
					jrp[i], jrp[j] = jrp[j], jrp[i]
					irp -= self.DistMatrix[i]
					jrp -= self.DistMatrix[j]
					if (np.linalg.norm(irp)+np.linalg.norm(jrp) < np.linalg.norm(ir)+np.linalg.norm(jr)):
						k = 0
						perm=range(m.NAtoms())
						perm[i] = j
						perm[j] = i
						tmp_coords=tmp_coords[perm]
						tmp_dm = MolEmb.Make_DistMat(tmp_coords)
						#print(np.linalg.norm(self.DistMatrix - tmp_dm))
						steps = steps+1
				#print(i)
			k+=1
		m.coords=tmp_coords.copy()
		#print("best",tmp_coords)
		#print("self",self.coords)
		self.WriteInterpolation(Mol(self.atoms,tmp_coords),10)
		return Mol(self.atoms,self.coords), Mol(self.atoms,tmp_coords)

# ---------------------------------------------------------------
#  Functions related to energy models and sampling.
#  all this shit should be moved into a "class Calculator"
# ---------------------------------------------------------------

	def BuildDistanceMatrix(self):
		self.DistMatrix = MolEmb.Make_DistMat(self.coords)

	def GoEnergy(self,x):
		''' The GO potential enforces equilibrium bond lengths. This is the lennard jones soft version'''
		if (self.DistMatrix is None):
			print("Build DistMatrix")
			raise Exception("dmat")
		xmat = np.array(x).reshape(self.NAtoms(),3)
		newd = MolEmb.Make_DistMat(xmat)
		newd -= self.DistMatrix
		newd = newd*newd
		return PARAMS["GoK"]*np.sum(newd)

	def GoForce(self, at_=-1, spherical = 0):
		'''
			The GO potential enforces equilibrium bond lengths, and this is the force of that potential.
			Args: at_ an atom index, if at_ = -1 it returns an array for each atom.
		'''
		if (spherical):
			rthph = MolEmb.Make_GoForce(self.coords,self.DistMatrix,at_,1)
			rthph[:,0] = rthph[:,0]*PARAMS["GoK"]
			return rthph
		else:
			return PARAMS["GoK"]*MolEmb.Make_GoForce(self.coords,self.DistMatrix,at_,0)

	def GoForceLocal(self, at_=-1):
		''' The GO potential enforces equilibrium bond lengths, and this is the force of that potential.
			A MUCH FASTER VERSION OF THIS ROUTINE IS NOW AVAILABLE, see MolEmb::Make_Go
		'''
		return PARAMS["GoK"]*MolEmb.Make_GoForceLocal(self.coords,self.DistMatrix,at_)

	def NumericGoHessian(self):
		if (self.DistMatrix==None):
			print("Build DistMatrix")
			raise Exception("dmat")
		disp=0.001
		hess=np.zeros((self.NAtoms()*3,self.NAtoms()*3))
		for i in range(self.NAtoms()):
			for j in range(self.NAtoms()):
				for ip in range(3):
					for jp in range(3):
						if (j*3+jp >= i*3+ip):
							tmp = self.coords.flatten()
							tmp[i*3+ip] += disp
							tmp[j*3+jp] += disp
							f1 = self.GoEnergy(tmp)
							tmp = self.coords.flatten()
							tmp[i*3+ip] += disp
							tmp[j*3+jp] -= disp
							f2 = self.GoEnergy(tmp)
							tmp = self.coords.flatten()
							tmp[i*3+ip] -= disp
							tmp[j*3+jp] += disp
							f3 = self.GoEnergy(tmp)
							tmp = self.coords.flatten()
							tmp[i*3+ip] -= disp
							tmp[j*3+jp] -= disp
							f4 = self.GoEnergy(tmp)
							hess[i*3+ip,j*3+jp] = (f1-f2-f3+f4)/(4.0*disp*disp)
		return (hess+hess.T-np.diag(np.diag(hess)))

	def GoHessian(self):
		return PARAMS["GoK"]*MolEmb.Make_GoHess(self.coords,self.DistMatrix)

	def ScanNormalModes(self,npts=11,disp=0.2):
		"These modes are normal"
		self.BuildDistanceMatrix()
		hess = self.GoHessian()
		w,v = np.linalg.eig(hess)
		thresh = pow(10.0,-6.0)
		numincl = np.sum([1 if abs(w[i])>thresh else 0 for i in range(len(w))])
		tore = np.zeros((numincl,npts,self.NAtoms(),3))
		nout = 0
		for a in range(self.NAtoms()):
			for ap in range(3):
				if (abs(w[a*3+ap])<thresh):
					continue
				tmp = v[:,a*3+ap]/np.linalg.norm(v[:,a*3+ap])
				eigv = np.reshape(tmp,(self.NAtoms(),3))
				for d in range(npts):
					tore[nout,d,:,:] = (self.coords+disp*(self.NAtoms()*(d-npts/2.0+0.37)/npts)*eigv).real
					#print disp*(self.NAtoms()*(d-npts/2.0+0.37)/npts)*eigv
					#print d, self.GoEnergy(tore[nout,d,:,:].flatten())#, PARAMS["GoK"]*MolEmb.Make_GoForce(tore[nout,d,:,:],self.DistMatrix,-1)
				nout = nout+1
		return tore

	def SoftCutGoForce(self, cutdist=6):
		if (self.DistMatrix==None):
			print("Build DistMatrix")
			raise Exception("dmat")
		forces = np.zeros((self.NAtoms(),3))
		for i in range(len(self.coords)):
			forces[i]=self.SoftCutGoForceOneAtom(i, cutdist)
		return forces

	def GoForce_Scan(self, maxstep, ngrid):
		#scan near by regime and return the samllest force
		forces = np.zeros((self.NAtoms(),3))
		TmpForce = np.zeros((self.NAtoms(), ngrid*ngrid*ngrid,3),dtype=np.float)
		for i in range (0, self.NAtoms()):
			print("Atom: ", i)
			save_i = self.coords[i].copy()
			samps=MakeUniform(self.coords[i],maxstep,ngrid)
			for m in range (0, samps.shape[0]):
				self.coords[i] = samps[m].copy()
				for j in range(len(self.coords)):
					# compute force on i due to all j's
					u = self.coords[j]-samps[m]
					dij = np.linalg.norm(u)
					if (dij != 0.0):
						u = u/np.linalg.norm(u)
					TmpForce[i][m] += 0.5*(dij-self.DistMatrix[i,j])*u
			self.coords[i] = save_i.copy()
			TmpAbsForce = (TmpForce[i,:,0]**2+TmpForce[i,:,1]**2+TmpForce[i,:,2]**2)**0.5
			forces[i] = samps[np.argmin(TmpAbsForce)]
		return forces

	def EnergyAfterAtomMove(self,s,i,Type="GO"):
		if (Type=="GO"):
			out = np.zeros(s.shape[:-1])
			MolEmb.Make_Go(s,self.DistMatrix,out,self.coords,i)
			return out
		else:
			raise Exception("Unknown Energy")

	#Most parameters are unneccesary.
	def OverlapEmbeddings(self, d1, coords, d2 , d3 ,  d4 , d5, i, d6):#(self,coord,i):
		return np.array([GRIDS.EmbedAtom(self,j,i) for j in coords])

	def FitGoProb(self,ii,Print=False):
		'''
		Generates a Go-potential for atom i on a uniform grid of 4A with 50 pts/direction
		And fits that go potential with the H@0 basis centered at the same point
		In practice 9 (1A) gaussians separated on a 1A grid around the sensory point appears to work for moderate distortions.
		'''
		Ps = self.POfAtomMoves(GRIDS.MyGrid(),ii)
		Pc = np.dot(GRIDS.MyGrid().T,Ps)
		if (Print):
			print("Desired Displacement", Pc)  # should equal the point for a Go-Model at equilibrium
		V=GRIDS.Vectorize(Ps)#,True)
		out = np.zeros(shape=(1,GRIDS.NGau3+3))
		out[0,:GRIDS.NGau3]+=V
		out[0,GRIDS.NGau3:]+=Pc
		return out

	def UseGoProb(self,ii,inputs):
		'''
		The opposite of the routine above. It takes the digested probability vectors and uses it to calculate desired new positions.
		'''
		pdisp=inputs[-3:]
		return pdisp

	def EnergiesOfAtomMoves(self,samps,i):
		return np.array([self.energyAfterAtomMove(s,i) for s in samps])

	def POfAtomMoves(self,samps,i):
		''' Arguments are given relative to the coordinate of i'''
		if (self.DistMatrix==None):
			raise Exception("BuildDMat")
		Es=np.zeros(samps.shape[0],dtype=np.float64)
		MolEmb.Make_Go(samps+self.coords[i],self.DistMatrix,Es,self.coords,i)
		Es=np.nan_to_num(Es)
		Es=Es-np.min(Es)
		Ps = np.exp(-1.0*Es/(0.25*np.std(Es)))
		Ps=np.nan_to_num(Ps)
		Z = np.sum(Ps)
		Ps /= Z
		return Ps

	def ForceFromXYZ(self, path):
		"""
		Reads the forces from the comment line in the md_dataset,
		and if no forces exist sets them to zero. Switched on by
		has_force=True in the ReadGDB9Unpacked routine
		"""
		try:
			f = open(path, 'r')
			lines = f.readlines()
			natoms = int(lines[0])
			forces=np.zeros((natoms,3))
			read_forces = ((lines[1].strip().split(';'))[1]).replace("],[", ",").replace("[","").replace("]","").split(",")
			for j in range(natoms):
				for k in range(3):
					forces[j,k] = float(read_forces[j*3+k])
			self.properties['forces'] = forces
		except Exception as Ex:
			print("Reading Force Failed.", Ex)

	def MMFF94FromXYZ(self, path):
		"""
		Reads the forces from the comment line in the md_dataset,
		and if no forces exist sets them to zero. Switched on by
		has_force=True in the ReadGDB9Unpacked routine
		TODO: Move this out of Mol please to AbInitio (JAP)
		"""
		try:
			f = open(path, 'r')
			lines = f.readlines()
			natoms = int(lines[0])
			forces=np.zeros((natoms,3))
			read_forces = ((lines[1].strip().split(';'))[3]).replace("],[", ",").replace("[","").replace("]","").split(",")
			for j in range(natoms):
				for k in range(3):
					forces[j,k] = float(read_forces[j*3+k])
			self.properties['mmff94forces'] = forces
		except Exception as Ex:
			print("Reading MMFF94 Force Failed.", Ex)

	def ChargeFromXYZ(self, path):
		"""
		Reads the forces from the comment line in the md_dataset,
		and if no forces exist sets them to zero. Switched on by
		has_force=True in the ReadGDB9Unpacked routine
		"""
		try:
			f = open(path, 'r')
			lines = f.readlines()
			natoms = int(lines[0])
			charges=np.zeros((natoms))
			read_charges = ((lines[1].strip().split(';'))[2]).replace("[","").replace("]","").split(",")
			for j in range(natoms):
				charges[j] = float(read_charges[j])
			self.properties['mulliken'] = charges
		except Exception as Ex:
			print("Reading Charges Failed.", Ex)


	def EnergyFromXYZ(self, path):
		"""
		Reads the energy from the comment line in the md_dataset.
		Switched on by has_energy=True in the ReadGDB9Unpacked routine
		"""
		try:
			f = open(path, 'r')
			lines = f.readlines()
			energy = float((lines[1].strip().split(';'))[0])
			self.properties['energy'] = energy
		except Exception as Ex:
			print("Reading Energy Failed.", Ex)

	def MakeBonds(self):
		self.BuildDistanceMatrix()
		maxnb = 0
		bonds = []
		for i in range(self.NAtoms()):
			for j in range(i+1,self.NAtoms()):
				if self.DistMatrix[i,j] < 3.0:
					bonds.append([i,j])
		bonds = np.asarray(bonds, dtype=np.int)
		self.properties["bonds"] = bonds
		self.nbonds = bonds.shape[0]
		f=np.vectorize(lambda x: self.atoms[x])
		self.bondtypes = np.unique(f(bonds), axis=0)
		return self.nbonds

	def BondTypes(self):
		return np.unique(self.bonds[:,0]).astype(int)

	def AtomName(self, i):
		return atoi.keys()[atoi.values().index(self.atoms[i])]

	def AllAtomNames(self):
		names=[]
		for i in range (0, self.atoms.shape[0]):
			names.append(atoi.keys()[atoi.values().index(self.atoms[i])])
		return names

	def Set_Qchem_Data_Path(self):
		self.qchem_data_path="./qchem"+"/"+self.properties["set_name"]+"/"+self.name
		return

	def Make_Spherical_Forces(self):
		self.properties["sphere_forces"] = CartToSphereV(self.properties["forces"])

	def MultipoleInputs(self):
		"""
			These are the quantities (in Atomic Units)
			which you multiply the atomic charges by (and sum)
			in order to calculate the multipoles of a molecule
			up to PARAMS["EEOrder"]

			Returns:
				(NAtoms X (monopole, dipole x, ... quad x... etc. ))
		"""
		tore = None
		com = self.Center(OfMass=True)
		if (PARAMS["EEOrder"] == 2):
			tore = np.zeros((self.NAtoms,4))
			for i in range(self.NAtoms()):
				tore[i,0] = 1.0
				tore[i,1:] = self.coords[i]-com
		else:
			raise Exception("Implement... ")
		return tore

class Frag_of_Mol(Mol):
	def __init__(self, atoms_=None, coords_=None):
		Mol.__init__(self, atoms_, coords_)
		self.atom_nodes = None
		self.undefined_bond_type =  None # whether the dangling bond can be connected  to H or not
		self.undefined_bonds = None  # capture the undefined bonds of each atom

	def FromXYZString(self,string, set_name = None):
		Mol.FromXYZString(self,string)
		self.properties["set_name"] = set_name
		return

	def Make_AtomNodes(self):
		atom_nodes = []
		for i in range (0, self.NAtoms()):
			if i in self.undefined_bonds.keys():
				atom_nodes.append(AtomNode(self.atoms[i], i,  self.undefined_bond_type, self.undefined_bonds[i]))
			else:
				atom_nodes.append(AtomNode(self.atoms[i], i, self.undefined_bond_type))
		self.atom_nodes = atom_nodes
		return
