"""
A periodic version of SimpleMD
No symmetry but general unit cells supported.

Maintenance of the unit cell, etc. are handled by PeriodicForce.
Only linear scaling forces with energy are supported.

TODO: Barostat...
"""

from __future__ import absolute_import
from __future__ import print_function
from .Sets import *
from .TFManage import *
from .Neighbors import *
from .Electrostatics import *
from .QuasiNewtonTools import *
from .Periodic import *
from .SimpleMD import *

def PeriodicVelocityVerletStep(pf_, a_, x_, v_, m_, dt_):
	"""
	A Periodic Velocity Verlet Step (just modulo's the vectors.)

	Args:
		pf_: The PERIODIC force class (returns Joules/Angstrom)
		a_: The acceleration at current step. (A^2/fs^2)
		x_: Current coordinates (A)
		v_: Velocities (A/fs)
		m_: the mass vector. (kg)
	Returns:
		x: updated positions
		v: updated Velocities
		a: updated accelerations
		e: Energy at midpoint per unit cell.
	"""
	x = x_ + v_*dt_ + (1./2.)*a_*dt_*dt_
	x = pf_.lattice.ModuloLattice(x)
	e, f_x_ = pf_(x)
	a = pow(10.0,-10.0)*np.einsum("ax,a->ax", f_x_, 1.0/m_) # m^2/s^2 => A^2/Fs^2
	v = v_ + (1./2.)*(a_+a)*dt_
	return x,v,a,e

class PeriodicNoseThermostat(NoseThermostat):
	def __init__(self,m_,v_):
		NoseThermostat.__init__(self,m_,v_)
		return
	def step(self, pf_, a_, x_, v_, m_, dt_ ):
		"""
		A periodic Nose thermostat velocity verlet step
		http://www2.ph.ed.ac.uk/~dmarendu/MVP/MVP03.pdf

		Args:
			pf_: a Periodic force class.
			a_: acceleration
			x_: coordinates
			v_: velocities
			m_: masses
			dt_: timestep.
		"""
		# Recompute these stepwise in case of variable T.
		self.kT = IDEALGASR*pow(10.0,-10.0)*self.T # energy units here are kg (A/fs)^2
		self.tau = 20.0*PARAMS["MDdt"]*self.N
		self.Q = self.kT*self.tau*self.tau
		x = x_ + v_*dt_ + (1./2.)*(a_ - self.eta*v_)*dt_*dt_
		x = pf_.lattice.ModuloLattice(x)
		vdto2 = v_ + (1./2.)*(a_ - self.eta*v_)*dt_
		e, f_x_ = pf_(x)
		a = pow(10.0,-10.0)*np.einsum("ax,a->ax", f_x_, 1.0/m_) # m^2/s^2 => A^2/Fs^2
		ke = (1./2.)*np.dot(np.einsum("ia,ia->i",v_,v_),m_)
		etadto2 = self.eta + (dt_/(2.*self.Q))*(ke - (((3.*self.N+1)/2.))*self.kT)
		kedto2 = (1./2.)*np.dot(np.einsum("ia,ia->i",vdto2,vdto2),m_)
		self.eta = etadto2 + (dt_/(2.*self.Q))*(kedto2 - (((3.*self.N+1)/2.))*self.kT)
		v = (vdto2 + (dt_/2.)*a)/(1 + (dt_/2.)*self.eta)
		return x,v,a,e

class PeriodicVelocityVerlet(VelocityVerlet):
	def __init__(self, Force_, name_ ="PdicMD", v0_=None):
		"""
		Molecular dynamics

		Args:
			Force_: A PERIODIC energy, force CLASS.
			PMol_: initial molecule.
			PARAMS["MDMaxStep"]: Number of steps to take.
			PARAMS["MDTemp"]: Temperature to initialize or Thermostat to.
			PARAMS["MDdt"]: Timestep.
			PARAMS["MDV0"]: Sort of velocity initialization (None, or "Random")
			PARAMS["MDLogTrajectory"]: Write MD Trajectory.
		Returns:
			Nothing.
		"""
		self.PForce = Force_
		VelocityVerlet.__init__(self, None, self.PForce.mol0, name_, self.PForce.__call__)
		if v0_ is not None:
			self.v = v0_
		if (PARAMS["MDThermostat"]=="Nose"):
			self.Tstat = PeriodicNoseThermostat(self.m,self.v)
		else:
			print("Unthermostated Periodic Velocity Verlet.")
		return
	def Density(self):
		"""
		Returns the density in g/cm**3 of the bulk.
		"""
		return self.PForce.Density()
	def WriteTrajectory(self):
		m=Mol(self.atoms,self.x)
		m.properties["Lattice"]=self.PForce.lattice.lattice.copy()
		m.properties["Time"]=self.t
		m.properties["KineticEnergy"]=self.KE
		m.properties["PotEnergy"]=self.EPot
		m.WriteXYZfile("./results/", "MDTrajectory"+self.name,'a',True)
		return
	def Prop(self):
		"""
		Propagate VelocityVerlet
		"""
		print ("begin Periodic VelocityVerlet")
		step = 0
		self.md_log = np.zeros((self.maxstep, 7)) # time Dipoles Energy
		while(step < self.maxstep):
			t = time.time()
			self.t = step*self.dt
			self.KE = KineticEnergy(self.v,self.m)
			Teff = (2./3.)*self.KE/IDEALGASR
			if (PARAMS["MDThermostat"]==None):
				self.x , self.v, self.a, self.EPot = PeriodicVelocityVerletStep(self.PForce, self.a, self.x, self.v, self.m, self.dt)
			else:
				self.x , self.v, self.a, self.EPot = self.Tstat.step(self.PForce, self.a, self.x, self.v, self.m, self.dt)
			self.md_log[step,0] = self.t
			self.md_log[step,4] = self.KE
			self.md_log[step,5] = self.EPot
			self.md_log[step,6] = self.KE+(self.EPot-self.EPot0)*JOULEPERHARTREE

			if (PARAMS["PrintTMTimer"]):
				PrintTMTIMER()
			if (step%1==0 and PARAMS["MDLogTrajectory"]):
				self.WriteTrajectory()
			if (step%500==0):
				np.savetxt("./results/"+"MDLog"+self.name+".txt",self.md_log)

			step+=1
			LOGGER.info("Step: %i time: %.1f(fs) <KE>(kJ/mol): %.5f <|a|>(m/s2): %.5f <EPot>(Eh): %.5f <Etot>(kJ/mol): %.5f Rho(g/cm**3): %.5f Teff(K): %.5f", step, self.t, self.KE/1000.0,  np.linalg.norm(self.a) , self.EPot, self.KE/1000.0+self.EPot*KJPERHARTREE,self.Density(), Teff)
			print(("per step cost:", time.time() -t ))
		return

class PeriodicBoxingDynamics(PeriodicVelocityVerlet):
	def __init__(self, Force_, BoxingLatp_=np.eye(3), name_ ="PdicBoxMD", BoxingT_= 400):
		"""
		Periodically Crushes a molecule by shrinking it's lattice to obtain a desired density.

		Args:
			Force_: A PeriodicForce object
			BoxingLatp_ : Final Lattice.
			BoxingT_: amount of time for the boxing dynamics in fs.
			PARAMS["MDMaxStep"]: Number of steps to take.
			PARAMS["MDTemp"]: Temperature to initialize or Thermostat to.
			PARAMS["MDdt"]: Timestep.
			PARAMS["MDV0"]: Sort of velocity initialization (None, or "Random")
			PARAMS["MDLogTrajectory"]: Write MD Trajectory.
		Returns:
			Nothing.
		"""
		self.PForce = Force_
		self.BoxingLat0 = Force_.lattice.lattice.copy()
		self.BoxingLatp = BoxingLatp_.copy()
		self.BoxingT = BoxingT_
		VelocityVerlet.__init__(self, None, self.PForce.mol0, name_, self.PForce.__call__)
		if (PARAMS["MDThermostat"]=="Nose"):
			self.Tstat = PeriodicNoseThermostat(self.m,self.v)
		else:
			print("Unthermostated Periodic Velocity Verlet.")
		return

	def Prop(self):
		"""
		Propagate VelocityVerlet
		"""
		step = 0
		self.md_log = np.zeros((self.maxstep, 7)) # time Dipoles Energy
		while(step < self.maxstep):
			t = time.time()
			self.t = step*self.dt
			self.KE = KineticEnergy(self.v,self.m)

			if (self.t>self.BoxingT):
				print("Exceeded Boxtime\n",self.BoxingLatp)
			else:
				newlattice = ((self.BoxingT-self.t)/(self.BoxingT))*self.BoxingLat0+(1.0-(self.BoxingT-self.t)/(self.BoxingT))*self.BoxingLatp
				self.x = self.PForce.AdjustLattice(self.x, self.PForce.lattice.lattice,newlattice)
				self.v = self.PForce.AdjustLattice(self.v, self.PForce.lattice.lattice,newlattice)
				self.a = self.PForce.AdjustLattice(self.a, self.PForce.lattice.lattice,newlattice)
				self.PForce.ReLattice(newlattice)
			print("Density:", self.Density())

			Teff = (2./3.)*self.KE/IDEALGASR
			if (PARAMS["MDThermostat"]==None):
				self.x , self.v, self.a, self.EPot = PeriodicVelocityVerletStep(self.PForce, self.a, self.x, self.v, self.m, self.dt)
			else:
				self.x , self.v, self.a, self.EPot = self.Tstat.step(self.PForce, self.a, self.x, self.v, self.m, self.dt)
			self.md_log[step,0] = self.t
			self.md_log[step,4] = self.KE
			self.md_log[step,5] = self.EPot
			self.md_log[step,6] = self.KE+(self.EPot-self.EPot0)*JOULEPERHARTREE

			if (step%3==0 and PARAMS["MDLogTrajectory"]):
				self.WriteTrajectory()
			if (step%500==0):
				np.savetxt("./results/"+"MDLog"+self.name+".txt",self.md_log)

			step+=1
			LOGGER.info("Step: %i time: %.1f(fs) <KE>(kJ/mol): %.5f <|a|>(m/s2): %.5f <EPot>(Eh): %.5f <Etot>(kJ/mol): %.5f Teff(K): %.5f", step, self.t, self.KE/1000.0,  np.linalg.norm(self.a) , self.EPot, self.KE/1000.0+self.EPot*KJPERHARTREE, Teff)
			print(("per step cost:", time.time() -t ))
		return


class PeriodicAnnealer(PeriodicVelocityVerlet):
	def __init__(self, Force_, name_ ="PdicAnneal",AnnealThresh_ = 0.000009):
		"""
		Anneals a periodic molecule.

		Args:
			Force_: A PeriodicForce object
			PARAMS["MDMaxStep"]: Number of steps to take.
			PARAMS["MDTemp"]: Temperature to initialize or Thermostat to.
			PARAMS["MDdt"]: Timestep.
			PARAMS["MDV0"]: Sort of velocity initialization (None, or "Random")
			PARAMS["MDLogTrajectory"]: Write MD Trajectory.
		Returns:
			Nothing.
		"""
		PeriodicVelocityVerlet.__init__(self, Force_, name_)
		self.dt = 0.1
		self.v *= 0.0
		self.AnnealT0 = PARAMS["MDAnnealT0"]
		self.AnnealSteps = PARAMS["MDAnnealSteps"]
		self.MinS = 0
		self.MinE = 99999999.0
		self.Minx = None
		self.AnnealThresh = AnnealThresh_
		self.Tstat = PeriodicNoseThermostat(self.m,self.v)
		return
	def Prop(self):
		"""
		Propagate VelocityVerlet
		"""
		step = 0
		self.md_log = np.zeros((self.maxstep, 7)) # time Dipoles Energy
		while(step < self.AnnealSteps):
			t = time.time()
			self.t = step*self.dt
			self.KE = KineticEnergy(self.v,self.m)
			Teff = (2./3.)*self.KE/IDEALGASR

			AnnealFrac = float(self.AnnealSteps - step)/self.AnnealSteps
			self.Tstat.T = self.AnnealT0*AnnealFrac + PARAMS["MDAnnealTF"]*(1.0-AnnealFrac) + pow(10.0,-10.0)

			self.x , self.v, self.a, self.EPot = self.Tstat.step(self.PForce, self.a, self.x, self.v, self.m, self.dt)

			if (self.EPot < self.MinE and abs(self.EPot - self.MinE)>self.AnnealThresh and step>1):
				self.MinE = self.EPot
				self.Minx = self.x.copy()
				self.MinS = step
				LOGGER.info("   -- cycling annealer -- ")
				if (PARAMS["MDAnnealT0"] > PARAMS["MDAnnealTF"]):
					self.AnnealT0 = self.Tstat.T+PARAMS["MDAnnealKickBack"]
				print(self.x)
				step=0

			self.md_log[step,0] = self.t
			self.md_log[step,4] = self.KE
			self.md_log[step,5] = self.EPot
			self.md_log[step,6] = self.KE+(self.EPot-self.EPot0)*JOULEPERHARTREE

			if (step%3==0 and PARAMS["MDLogTrajectory"]):
				self.WriteTrajectory()
			if (step%500==0):
				np.savetxt("./results/"+"MDLog"+self.name+".txt",self.md_log)

			step+=1
			LOGGER.info("Step: %i time: %.1f(fs) <KE>(kJ/mol): %.5f <|a|>(m/s2): %.5f <EPot>(Eh): %.5f <Etot>(kJ/mol): %.5f Rho(g/cm3) %.5f Teff(K): %.5f T_target(K): %.5f", step, self.t, self.KE/1000.0,  np.linalg.norm(self.a) , self.EPot, self.KE/1000.0+self.EPot*KJPERHARTREE, self.Density(),  Teff, self.Tstat.T)
			print(("per step cost:", time.time() -t ))
		Mol(self.atoms,self.Minx).WriteXYZfile("./results","PAnnealMin",wprop = True)
		return
