from __future__ import absolute_import
from __future__ import print_function
from .Sets import *
from .TFManage import *

class DIIS:
	def __init__(self, ForceAndEnergy_, x0_=None):
		"""
		Simplest Possible DIIS
		"""
		self.m_max = PARAMS["DiisSize"]
		self.n_now = 0
		self.v_shp = None
		self.Vs = None
		self.Rs = None
		self.M = np.zeros((self.m_max+1,self.m_max+1))
		self.S = np.zeros((self.m_max+1,self.m_max+1)) # Overlap matrix.
		self.EForce = ForceAndEnergy_
		return
	def __call__(self, new_vec_):
		"""
		Iterate BFGS

		Args:
			new_vec_: Point at which to minimize gradients
		Returns:
			Next point, energy, and gradient.
		"""
		e,g = self.EForce(new_vec_)
		return self.NextStep(new_vec_, g), e, g
	def NextStep(self, new_vec_, new_residual_):
		if (self.n_now == 0):
			self.v_shp = new_vec_.shape
			self.Vs = np.zeros([self.m_max]+list(self.v_shp))
			self.Rs = np.zeros([self.m_max]+list(self.v_shp))
		if (self.n_now<self.m_max):
			self.Vs[self.n_now] = new_vec_.copy()
			self.Rs[self.n_now] = new_residual_.copy()
			for i in range(self.n_now):
				self.S[i,self.n_now] = np.dot(self.Rs[i].flatten(),new_residual_.flatten())
				self.S[self.n_now,i] = self.S[i,self.n_now]
			self.S[self.n_now,self.n_now] = np.dot(new_residual_.flatten(),new_residual_.flatten())
			self.n_now += 1
		else:
			self.Vs = np.roll(self.Vs,-1,axis=0)
			self.Rs = np.roll(self.Rs,-1,axis=0)
			self.S = np.roll(np.roll(self.S,-1,axis=0),-1,axis=1)
			self.Vs[-1] = new_vec_.copy()
			self.Rs[-1] = new_residual_.copy()
			for i in range(self.n_now):
				self.S[i,self.n_now] = np.dot(self.Rs[i].flatten(),new_residual_.flatten())
				self.S[self.n_now,i] = self.S[i,self.n_now]
			self.S[self.n_now,self.n_now] = np.dot(new_residual_.flatten(),new_residual_.flatten())
		if (self.n_now<2):
			return new_vec_ + 0.02*new_residual_
		#print "S", self.S[:self.n_now,:self.n_now]
		#print "Vs: ", self.Vs
		#print "Rs: ", self.Rs
		# Build the DIIS matrix which has dimension n_now + 1
		self.M *= 0.0
		scale_factor = 1.0#/self.S[0,0]
		for i in range(self.n_now):
			for j in range(self.n_now):
				self.M[i,j] = self.S[i,j] * scale_factor
		self.M[self.n_now,:] = -1.0
		self.M[:,self.n_now] = -1.0
		self.M[self.n_now,self.n_now] = 0.0
		#print self.M[:self.n_now+1,:self.n_now+1]
		# Solve the DIIS problem.
		tmp = np.zeros(self.n_now+1)
		tmp[self.n_now]=-1.0
		U, s, V = np.linalg.svd(self.M[:self.n_now+1,:self.n_now+1]) #M=u * np.diag(s) * v,
		# Filter small values.
		#print "s", s
		for i in range(len(s)):
			if (s[i]!=0.0 and abs(s[i])>0.0000001):
				s[i]=1.0/s[i]
			else:
				s[i] = 0.0
		#print "Diis inv: ", (U*s*V)
		next_coeffs = np.dot(np.dot(np.dot(U,np.diag(s)),V),tmp)
		print("DIIS COEFFs: ", next_coeffs)
		#next_coeffs = np.dot(np.linalg.inv(self.M[:self.n_now+1,:self.n_now+1]),tmp)
		#print next_coeffs.shape
		tore = np.zeros(new_vec_.shape)
		for i in range(self.n_now):
			tore += self.Vs[i]*next_coeffs[i]
		return tore
