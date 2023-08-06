# -*- coding: utf-8 -*-
"""
Class representing aggregates of molecules.

The class enables building of complicated objects from objects of the Molecule
type, their mutual interactions and system-bath interactions. It also provides
an interface to various methods of open quantum systems theory.


"""

import numpy
#import h5py

from ..core.managers import UnitsManaged
from ..core.units import cm2int
from .interactions import dipole_dipole_interaction

from ..qm.oscillators.ho import fcstorage
from ..qm.oscillators.ho import operator_factory

from ..qm.hilbertspace.operators import Operator
from ..qm.hilbertspace.operators import DensityMatrix
from ..qm.liouvillespace.systembathinteraction import SystemBathInteraction
from ..qm.hilbertspace.hamiltonian import Hamiltonian
from ..qm.hilbertspace.dmoment import TransitionDipoleMoment

from ..qm.corfunctions import CorrelationFunctionMatrix

from ..spectroscopy import diagramatics as diag

#from .aggregate_states import aggregate_state
from .aggregate_states import electronic_state
from .aggregate_states import vibronic_state

#from ..core.managers import energy_units
#from .molecules import Molecule
from ..core.managers import Manager
from ..core.saveable import Saveable

          
class Aggregate(UnitsManaged, Saveable):
    """ Molecular aggregate 
    
    
    Parameters
    ----------
    
    name : str
        Specifies the name of the aggregate
        
    molecules : list or tuple
        List of molecules out of which the aggregate is built
    
    """
    
    def __init__(self, molecules=None, name=""):

        self.mnames = {}    #
        self.monomers = []   
        self.nmono = 0         #
        self.name = name       #
        self.mult = 0          #

        self._has_egcf_matrix = False #
        self.egcf_matrix = None
        
        self._has_system_bath_interaction = False #
        
        self.coupling_initiated = False #
        self.resonance_coupling = None
        
        if molecules is not None:
            for m in molecules:
                self.add_Molecule(m)
                
        self._init_me()  


    def _init_me(self):
        """Initializes all built attributes of the aggregate
        
        This should put the object into a pre-build state
        
        
        """

        self.FC = fcstorage()
        self.ops = operator_factory()
        
        self._has_relaxation_tensor = False #
        
        self._relaxation_theory = "" #
        
        self._built = False     #
        
        self.mult = 0                #
        self.sbi_mult = 0            #
        self.Nel = 0                 #
        self.Ntot = 0                #
        self.Nb = 0                  #
        
        self.vibindices = []
        self.which_band = None
        self.elsigs = None
        
        self.HH = None
        self.HamOp = None
        self.DD = None
        self.D2 = None
        self.D2_max = 0
        self.sbi = None
        
        
    def clean(self):
        """Cleans the aggregate object of anything built
        
        This operation leaves the molecules of the aggregate intact and keeps
        few more pieces of information it it. E. g. coupling matrix is not 
        deleted. You call build again after this.
        
        
        """
        self._init_me()
        
    
    def wipe_out(self):
        """Removes everything except of name attribute
        
        You have to set molecules and recalculate interactions before you can
        build
        
        
        """
        self.mnames = {}   #
        self.monomers = []
        self.nmono = 0      #
        self.mult = 0       #
        self.sbi_mult = 0    #

        self._has_egcf_matrix = False   #
        self.egcf_matrix = None
        
        self._has_system_bath_interaction = False  #
       
        self.coupling_initiated = False     #
        self.resonance_coupling = None    #
        
        self._init_me()        


    def _before_save(self):
        self.manager = None


    def _after_save(self):
        self.manager = Manager()


    def _after_load(self):
        self.manager = Manager()
        

    ########################################################################
    #
    #    BUILDING METHODS
    #
    ########################################################################

    def init_coupling_matrix(self):
        """Nullifies coupling matrix
        
        
        """
        self.resonance_coupling = numpy.zeros((self.nmono,self.nmono),
                                              dtype=numpy.float64) 
        self.coupling_initiated = True           
        
    def set_resonance_coupling(self, i, j, coupling):
        """Sets resonance coupling value between two sites
        
        """
        if not self.coupling_initiated:
            self.init_coupling_matrix() 
            
        coup = self.convert_energy_2_internal_u(coupling)
        
        self.resonance_coupling[i,j] = coup
        self.resonance_coupling[j,i] = coup
        
    def get_resonance_coupling(self, i, j):
        """Returns resonance coupling value between two sites
        
        """
        coupling = self.resonance_coupling[i,j]
        return self.convert_energy_2_current_u(coupling)
    
    def set_resonance_coupling_matrix(self,coupmat): 
        """Sets resonance coupling values from a matrix
        
        """

        if type(coupmat) in (list, tuple):
            coupmat = numpy.array(coupmat)
            
        coup = self.convert_energy_2_internal_u(coupmat)           
        self.resonance_coupling = coup 
        if not self.coupling_initiated:
            self.coupling_initiated = True
            
    def dipole_dipole_coupling(self, kk, ll, epsr=1.0):
        """Calculates dipole-dipole coupling 
        
        """
        if kk == ll:
            raise Exception("Only coupling between different molecules \
            can be calculated")
        
        #FIXME: this works only for first excited states of two-level molecules
        d1 = self.monomers[kk].dmoments[0,1,:]
        r1 = self.monomers[kk].position
        d2 = self.monomers[ll].dmoments[0,1,:]
        r2 = self.monomers[ll].position        

        return dipole_dipole_interaction(r1, r2, d1, d2, epsr)            

    def set_coupling_by_dipole_dipole(self, epsr=1.0):
        """Sets resonance coupling by dipole-dipole interaction
        
        """
        
        if not self.coupling_initiated:
            self.init_coupling_matrix() 
        for kk in range(self.nmono):
            for ll in range(kk+1,self.nmono):
                cc = self.dipole_dipole_coupling(kk,ll,epsr=epsr)
                self.resonance_coupling[kk,ll] = cc
                self.resonance_coupling[ll,kk] = cc
                
    def calculate_resonance_coupling(self, method="dipole-dipole",
                               params=dict(epsr=1.0)):
        """ Sets resonance coupling calculated by a given method 
        
        Parameters
        ----------
        
        method: string
            Method to be used for calculation of resonance coupling
            
        """
        pass
        
                
    def set_egcf_matrix(self,cm):
        """Sets a matrix describing system bath interaction
        
        """
        self.egcf_matrix = cm
        self._has_egcf_matrix = True
    
    #
    # Monomer
    #
    def add_Molecule(self,mono):
        """Adds monomer to the aggregate
        
        
        """
        
        # If at least one monomer has energy gap correlation function
        # we will try to build system bath interaction for a the aggregate.
        # Exception will be thrown if not all monomers have the same egcf
        if mono._has_egcf:
            self._has_system_bath_interaction = True
            
        self.monomers.append(mono)
        self.mnames[mono.name] = len(self.monomers)-1
        self.nmono += 1
        
    def get_Molecule_by_name(self,name):
        try:
            im = self.mnames[name]
            return self.monomers[im]
        except:
            raise Exception()        
        
    def remove_Molecule(self, mono):
        self.monomers.remove(mono)
        self.nmono -= 1

        
            
    def get_nearest_Molecule(self,molecule):
        """Returns a molecule nearest in the aggregate to a given molecule
        
        Parameters
        ----------
        
        molecule : Molecule
            Molecule whose neighbor we look for
        
        """
        tol = 1.0e-3
        rmin = 1.0e20
        r1 = molecule.position
        mmin = None
        for m in self.monomers:
            r2 = m.position
            r = r1 - r2
            dist = numpy.sqrt(numpy.dot(r,r))
            if (dist > tol) and (dist < rmin):
                mmin = m
                rmin = dist
                
        return mmin, rmin        
            
    #
    # Vibrational modes
    #
    def add_Mode_by_name(self,name,mode):
        try:
            im = self.mnames[name]
            mn = self.monomers[im]
            mn.add_mode(mode)
        except:
            raise Exception()
            
    def get_Mode_by_name(self,name,N):
        try:
            im = self.mnames[name]
            mn = self.monomers[im]
            return mn.get_mode(N)
        except:
            raise Exception("Mode not found")   
            
    #
    # Transition dipole
    #
    def get_dipole_by_name(self,name,N,M):
        try:
            im = self.mnames[name]
            mn = self.monomers[im]
            return mn.get_dipole(N,M)
        except:
            raise Exception()
            
    def get_dipole(self,n,N,M):
        nm = self.monomers[n]
        return nm.get_dipole(N,M)
    
    
    def get_max_excitations(self):
        """Returns a list of maximum number of excitations on each monomer
        
        """
        omax = []
        for nm in self.monomers:
            omax.append(nm.nel-1)
        return omax
        
  
    def get_energy_by_name(self, name, N):
        """ Electronic energy """
        try:
            im = self.mnames[name]
            mn = self.monomers[im]
            return mn.get_energy(N)
        except:
            raise Exception()

    
    def fc_factor(self,state1,state2):
        """Franck-Condon factors between two vibrational states
        
        
        Calculates Franck-Condon factor between two aggregate_states
        regardless of their electronic parts
        
        
        """
        
        inx1 = state1.vsig
        inx2 = state2.vsig
        sta1 = state1.elstate.vibmodes
        sta2 = state2.elstate.vibmodes

        if not (len(sta1)==len(sta2)):
            raise Exception("Incompatible states")
            
        res = 1.0
        for kk in range(len(sta1)):
            smod1 = sta1[kk]
            smod2 = sta2[kk]
            
            # difference in shifts
            shft = smod1.shift - smod2.shift
            # quantum numbers
            qn1 = inx1[kk]
            qn2 = inx2[kk]
            
            """calculate FC factors
            
            Best implementation would be a table look-up. First we calculate
            a table of FC factors from known omegas and shifts and here we
            just consult the table.
            
            """
            if not self.FC.lookup(shft):
                fc = self.ops.shift_operator(shft)[:20,:20]
                self.FC.add(shft,fc)
                
            ii = self.FC.index(shft)
            rs = self.FC.get(ii)[qn1,qn2]
            
            res = res*rs
            
        return res
    
    def transition_dipole(self,state1,state2):
        """ Transition dipole moment between two states 
        
        Parameters
        ----------
        state1 : class vibronic_state
            state 1
            
        state2 : class vibronic_state
            state 2 
        
        """
        
        # get electronic signatures
        els1 = state1.elstate.elsignature
        els2 = state2.elstate.elsignature  
        
        # only states in neighboring bands can be connected by dipole moment
        b1 = state1.elstate.band
        b2 = state2.elstate.band
        if (abs(b1-b2) != 1):
            return 0.0
        
        # count the number of differences
        l = 0
        count = 0
        for kk in els1:
            if kk != els2[l]:
                count += 1
            l += 1
                
                
        if count != 1:
            return 0.0
        
        # now that we know that the states differ by one excitation, let
        # us find on which molecule it is
        exstate = None
        l = -1
        for kk in els1: # signature is just a tuple; iterate over it  
            l += 1
            if kk != els2[l]: # this is the index where they differ
                # which of them is excited
                if kk > els2[l]:
                    exstate = els1
                else:
                    exstate = els2
                exindx = l

            
            
        if exstate is None:
            raise Exception()
        

        eldip = self.get_dipole(exindx,0,1)
        
#        eldip = 0.0
#        for kk in range(len(exstate)):
#            if (exstate[kk] == 1):
#                eldip = self.get_dipole(kk,1)
           
        # Franck-Condon factor between the two states
        fcfac = self.fc_factor(state1,state2)
       
        
        return eldip*fcfac
    
        
    def total_number_of_states(self, mult=1, vibgen_approx=None):
        """ Total number of states in the aggregate"""
        
        nret = 0
        
        for elsig in self.elsignatures(mult=mult):
            
            cs = electronic_state(self, elsig)
            
            if vibgen_approx is None:
                nv = 1
                # here we assume all available states
                for mn in cs.vibmodes:
                    nv *= mn.nmax

            elif vibgen_approx == "SPA":
                nv = 1
                # here only on state per mode in adition to the ground state is
                # allowed
                for mn in cs.vibmodes: 
                    nv += 1
                    
            nret += nv
                
        return nret

    def total_number_of_electronic_states(self,mult=1):
        """ Total number of electronic states in the aggregate"""
        
        nret = 0
        
        for elsig in self.elsignatures(mult=mult):
            nret += 1
            
        return nret

 
    def number_of_states_in_band(self, band=1, vibgen_approx=None):
        """ Number of states in a given excitonic band """
        
        nret = 0
        
        for elsig in self.elsignatures(mult=band, mode="EQ"):
            cs = electronic_state(self,elsig)
            if vibgen_approx is None:
                nv = 1
                # here we assume all available states
                for mn in cs.vibmodes:
                    nv *= mn.nmax

            elif vibgen_approx == "SPA":
                nv = 1
                # here only on state per mode in adition to the ground state is
                # allowed
                for mn in cs.vibmodes: 
                    nv += 1
                    
            nret += nv
            
        return nret
    
    def number_of_electronic_states_in_band(self,band=1):
        """ Number of states in a given excitonic band """
        
        nret = 0
        
        for elsig in self.elsignatures(mult=band,mode="EQ"):
            #cs = electronic_state(self,elsig)
            nv = 1
            #for mn in cs.vibmodes:
            #    nv *= mn.nmax
            nret += nv
            
        return nret
    
    
    def get_electronic_state(self, sig, index=0):
        return electronic_state(self, sig, index)
    
    
    def coupling(self, state1, state2):
        """Coupling between two aggregate states 
        
        
        
        """
        
        # Coupling between two purely electronic states
        if (isinstance(state1,electronic_state) 
           and isinstance(state2,electronic_state)):
            i = state1.index
            j = state2.index
            
            if self.nmono > 1:
                return self.resonance_coupling[i-1,j-1]
            else:
                return 0.0
            
        # Coupling between two general states
        elif (isinstance(state1,vibronic_state) 
          and isinstance(state2,vibronic_state)):
              
            es1 = state1.elstate
            es2 = state2.elstate
            
            fc = self.fc_factor(state1,state2)
            
            # it make sense to calculate coupling only when the number
            # of molecules is larger than 1
            if self.nmono > 1:

                # coupling within the bands
                if es1.band == es2.band:
                    
                    # single exciton band
                    if es1.band == 1:
                        kk = es1.index - 1
                        ll = es2.index - 1
                    
                        if (kk >= 0) and (ll >= 0):
                            coup = self.resonance_coupling[kk,ll]*fc
                        else:
                            coup = 0.0
                    else:
                        
                        els1 = es1.elsignature
                        els2 = es2.elsignature
                        Ns = len(els1)
                        sites = [0,0]
                        k = 0
                        # count differences
                        for i in range(Ns):
                            if els1[i] != els2[i]:
                                if (k == 0) or (k == 1):
                                    sites[k] = i
                                k += 1
                        # if there are exactly 2 differences, the differing
                        # two molecules are those coupled; sites[k] contains
                        # indiced those coupled molecules
                        if k == 2:
                            kk = sites[0]
                            ll = sites[1]
                            coup = self.resonance_coupling[kk,ll]*fc    
                        else:
                            coup = 0.0
                        
                else:
                    coup = 0.0
            else:
                coup = 0.0
            
            return coup
    
    
    
    #######################################################################
    #
    # Generators
    #
    #######################################################################

    def elsignatures(self, mult=1, mode="LQ"):
        """ Generator of electronic signatures 
        
        Here we create signature tuples of electronic states. The signature
        is a tuple with as many integer numbers as the members of
        the aggregate. Each integer represents the state in which the 
        member of the aggregate is, e.g. 0 for ground state, 1 for the first
        excited state etc.
        
        
        Parameters
        ----------
        mult : int
            multiplicity of excitons
            
        mode : str {"LQ", "EQ"}
            mode of the functions.
            
            mode="LQ" returns all signatures of states with 
            multiplicity less than or equal to the `mult`  
           
            mode="EQ" returns signatures of states with a multiplicity
            given by `mult`
            
        """

        if mode not in ["LQ","EQ"]:
            raise Exception("Unknown mode")
            
        l = len(self.monomers)

        # list of maximum numbers of excitations on each sites
        omax = self.get_max_excitations()
        
        if mult < 0:
            raise Exception("mult must be larger than or equal to zero")
            
        mlt = 0
        # iterate over all excition multiplicities
        while mlt <= mult:
            # no excitations (ground state)
            out = [0 for k in range(l)]
            # if this is the multiplicity 0, yield the ground state
            if (((mlt == 0) and (mode == "LQ")) or (mult==0)):
                yield tuple(out)
            else:
                k = 1
                # first we have only ground state signature
                ins = [out]
                strt = [0]
                while k <= mlt:
                    nins = [] 
                    nstr = []
                    # take all signatures in "ins" and add one excitation
                    for out_added, last in self._add_excitation(ins,strt,omax):
                        # if mlt excitation was added yield
                        if (((k == mlt) and (mode == "LQ"))
                          or((mult == k) and (mult == mlt))): 
                            yield tuple(out_added)
                        else:
                            # make a list of all new signatures
                            nins.append(out_added)
                            # for each signature, save the index
                            # on which an excitation was added last
                            nstr.append(last)
                    # set the new signatures for processing in the iteration
                    ins = nins
                    strt = nstr
                    k += 1
            mlt += 1
            
                    
    def _add_excitation(self,inlists,strt,omax):
        """Adds one excitation to all submitted electronic signatures"""
        
        k = 0
        # go through all signatures
        for inlist in inlists:
            l = len(inlist)
            if len(omax) != l:
                raise Exception("arg omax has to be a list of the same \
                length as arg inlist")
            # go through all positions from the last index on (in order 
            # to create unique signatures)
            for i in range(strt[k],l):
                # if it is possible to add and excitation
                # make a new list and add
                if inlist[i] < omax[i]:
                    out = inlist.copy()
                    out[i] += 1
                    # yield the list and the index of the last added exitation
                    yield out, i  
            k += 1

    
    def vibsignatures(self, elsignature, approx=None):
        """ Generator of vibrational signatures 
        
        Parameters
        ----------
        
        approx : None or str
            Approximation used in generation of vibrational states
            Allowed values are None or "SPA"
            
        """
        cs = electronic_state(self,elsignature)
        return cs.vsignatures(approx=approx)
    
    
    def allstates(self, mult=1, all_vibronic=True, 
                  save_indices=False, vibgen_approx=None):
        """ Generator of all states aggregate states
        
        
        """
        a = 0
        i = 0
        # run over all electronic signatures
        for ess1 in self.elsignatures(mult=mult):
            es1 = self.get_electronic_state(ess1,i)
            for vsig1 in es1.vsignatures(approx=vibgen_approx):
                if all_vibronic:
                    s1 = vibronic_state(es1,vsig1)
                else:
                    if vsig1:
                        s1 = vibronic_state(es1,vsig1)
                    else:
                        s1 = es1
                        
                if save_indices:
                    self.vibindices[i].append(a)
    
                yield a,s1
                a += 1
                
            if save_indices:
                self.elsigs[i] = ess1
                self.which_band[i] = numpy.sum(ess1)
            i += 1 # count electronic states
            

    def elstates(self):
        """ Generator of electronic states 
        
        """
        a = 0
        for ess1 in self.elsignatures():
            es1 = self.get_electronic_state(ess1)
            yield a,es1
            a += 1
        

    
    def __str__(self):
        out  = "\nquantarhei.Aggregate object"
        out += "\n==========================="
        out += "\nname = %s" % self.name
        out += "\nnumber of molecules = %i " % self.nmono
        count = 0
        for nm in self.monomers:
            out += "\n\nMonomer %i" % count 
            out += str(nm)
            count += 1
            
        out += "\n\nResonance coupling matrix: "
        out +=   "\n-------------------------- "
        out += "\n"+str(self.resonance_coupling)
            
        out += "\n\nAggregate built = "+str(self._built)
        
        out +="\n\nSelected attributes"
        out +="\n--------------------"
        out +="\nmult = "+str(self.mult)
        out +="\nNel  = "+str(self.Nel)
        out +="\nNtot = "+str(self.Ntot)
        
        
        return out
            
            
    
    #######################################################################
    #
    #    BUILDING
    #
    #######################################################################
        
    def build(self, mult=1, sbi_for_higher_ex=False, vibgen_approx=None):
        """Builds aggregate properties
        
        Calculates Hamiltonian and transition dipole moment matrices and
        sets up system-bath interaction 
        
        Parameters
        ----------
        
        mult : int
            exciton multiplicity
            
        sbi_for_higher_ex: bool
            If set True, system-bath information is explicitely created for
            higher exciton states (consistent with the specified parameters
            `mult`). If set False, it is expected that if system-bath
            interaction for higher excitons is needed, it will be reconstructed
            from the single exciton part of this object
            
        vibge_approx: 
            Approximation used in the generation of vibrational state.
        
        """
        
        # maximum multiplicity of excitons handled by this aggregate
        self.mult = mult 
        if sbi_for_higher_ex:
            self.sbi_mult = mult
        else:
            self.sbi_mult = 1
        
        #
        # Electronic and vibrational states
        #
        self.Nel = self.total_number_of_electronic_states(mult=mult)
        self.vibindices = []
        for i in range(self.Nel):
            self.vibindices.append([])
        
        # number of states in the aggregate (taking into account approximations
        # in generation of vibrational states)
        Ntot = self.total_number_of_states(mult=mult, 
                                           vibgen_approx=vibgen_approx)
        self.Ntot = Ntot
        self.which_band = numpy.zeros(self.Ntot, dtype=numpy.int)
        self.elsigs = [None]*self.Nel

        # Hamiltonian matrix        
        HH = numpy.zeros((Ntot, Ntot), dtype=numpy.float64)
        
        # Transition dipole moment matrix
        DD = numpy.zeros((Ntot, Ntot, 3),dtype=numpy.float64)
        
        # Initialization of the matrix of couplings between states
        if not self.coupling_initiated:    
            self.init_coupling_matrix()            
            
        # Set up Hamiltonian and Transition dipole moment matrices
        for a, s1 in self.allstates(mult=self.mult, save_indices=True,
                                    vibgen_approx=vibgen_approx):
            #print("state = ", a)
            HH[a,a] = s1.energy()
            for b,s2 in self.allstates(mult=self.mult,
                                    vibgen_approx=vibgen_approx):       
                DD[a,b,:] = self.transition_dipole(s1,s2)
                
                #print(" - ", a,b,s1.signature(),s2.signature())
                #print("  :", DD[a,b,:] )
                
                if a != b:
                    HH[a,b] = self.coupling(s1,s2) 
    
        #raise Exception()
        
        
        # Storing Hamiltonian and dipole moment matrices
        self.HH = HH
        self.HamOp = Hamiltonian(data=HH)

        self.DD = DD
        
        # squares of transition dipoles
        dd2 = numpy.zeros((Ntot,Ntot),dtype=numpy.float64)
        for a in range(Ntot):
            for b in range(Ntot):
                dd2[a,b] = numpy.dot(self.DD[a,b,:],self.DD[a,b,:])
        #
        self.D2 = dd2
        self.D2_max = numpy.max(dd2)
    
        # Number of states in individual bands      
        self.Nb = numpy.zeros(self.mult+1,dtype=numpy.int)
        for ii in range(self.mult+1):
            self.Nb[ii] = self.number_of_states_in_band(band=ii,
            vibgen_approx=vibgen_approx)
       
        
        #######################################################################
        #
        # System-bath coupling
        #
        #######################################################################
            
        #FIXME: What to do when correlation functions are used for
        # an aggregate with vibrations
 
        if self._has_egcf_matrix:
            
            # Check the consistency of the energy gap correlation matrix
            if self.egcf_matrix.nob != self.nmono:
                raise Exception("Correlation matrix has a size different" + 
                                " from the number of monomers")
            for i in range(self.nmono):
                if not (self.monomers[i].egcf_matrix is self.egcf_matrix):
                    raise Exception("Correlation matrix in the monomer" +
                                    " has to be the same as the one of" +
                                    " the aggregate.")
            # seems like everything is consistent -> we can calculate system-
            # -bath interaction
            self._has_system_bath_interaction = True   
                     
        # try to get one from monomers
        else:
            
#            nm = self.monomers[0]
#            # FIXME: This is depricated - monomers do not need egcf_matrix
#            if nm._has_egcf_matrix:
#                self.egcf_matrix = nm.egcf_matrix
#                for i in range(self.nmono):
#                    if not (self.monomers[i].egcf_matrix is self.egcf_matrix):
#                        raise Exception("Correlation matrix in the" + 
#                                        " monomer has to be the same as" +
#                                        " the one of the aggregate.")
#                                                                                
#                # seems like everything is consistent -> we can calculate
#                # system--bath interaction
#                self._has_system_bath_interaction = True
#                self._has_egcf_matrix = True
#                
#            else:
                # probably we will not be dealing with an open system
                # do not set system-bath interaction
                #raise Exception("Monomer(s) have no egcf matrix")
            self._has_system_bath_interaction = False
            
        # try to set energy gap correlation matrix from monomers
        if not self._has_system_bath_interaction:   
            
            # if it has no correlation function we cannot calculate anything
            egcf_ok = True
            try:
                egcf1 = self.monomers[0].get_transition_environment((0,1))
            except:
                egcf_ok = False 
            
            if egcf_ok:
                # time axis of the first monomer
                time = egcf1.axis  
                # Number of correlation functions is the number of electronic
                # states minus ground state (this assumes that only electronic
                # states are coupled to the bath)
                Nelg = 1                
                if sbi_for_higher_ex:
                    Ncf = self.Nel - Nelg
                else:
                    Ncf = self.nmono
                    
                self.egcf_matrix = CorrelationFunctionMatrix(time, Ncf)
                
                for i in range(self.Nel):
                    
                    if self.which_band[i] == 1:
                        j = i - Nelg
                        mon = self.monomers[j]
                        cfce = mon.get_transition_environment((0,1))

                        mapi = self.egcf_matrix.set_correlation_function(cfce,
                                                                     [(j,j)])
                    
                        if mapi <= 0:
                            raise Exception("Something's wrong")
                                                
                        # FIXME: is this needed???
#                        mon.unset_transition_environment((0,1))
#                        mon.set_egcf_mapping((0,1), self.egcf_matrix, j)
                        
                    elif (self.which_band[i] == 2) and sbi_for_higher_ex:
                        l = i - Nelg
                        j = self.elsigs[i][0]
                        k = self.elsigs[i][1]
                        mon1 = self.monomers[j]
                        mon2 = self.monomers[k]
                        cfce1 = mon1.get_transition_environment((0,1)) 
                        cfce2 = mon2.get_transition_environment((0,1))
                        
                        cfce = cfce1 + cfce2

                        mapi = self.egcf_matrix.set_correlation_function(cfce,
                                                                     [(l,l)])
                        
                        # FIXME: cross-correlation between double excitons
                        # needs to be handled.
                    
                        if mapi <= 0:
                            raise Exception("Something's wrong")

                    elif (self.which_band[i] == 2) and (not sbi_for_higher_ex):
                        # this should be handled by
                        # a map between double excitons and site cor. functions
                        pass
                        
                    elif (self.which_band[i] > 2) and sbi_for_higher_ex:
                        pass
                    
                self._has_system_bath_interaction = True
                self._has_egcf_matrix = True   
                
            
        if self._has_system_bath_interaction:
            
            # interaction operators
            iops = []

            # How many operators should be created
            if sbi_for_higher_ex:
                Nop = self.Nel-1 # all electronic states
            else:
                Nop = self.Nb[1] # we count only single excited states

            # if there are more states in the single exciton block
            # than the number of sites, it means we have vibrational states
            if self.nmono != self.Nb[1]:
                
                for i in range(self.Nop): #range(0,self.nmono):
                    op1 = Operator(dim=self.HH.shape[0],real=True)
                    # here we make a projector on the subspace defined
                    # by a given electronic state |i>
                    for j in self.vibindices[i]:
                        op1.data[j,j] = 1.0
                    iops.append(op1)      
                  
            # standard case with only electronic states
            else:

                for i in range(1,Nop+1): 
                    op1 = Operator(dim=self.HH.shape[0],real=True)
                    op1.data[i,i] = 1.0
                    iops.append(op1)
                
            self.sbi = SystemBathInteraction(iops,
                                self.egcf_matrix,system=self)  
                                                 
        else:
            pass #$print("System bath interaction not set")
            
        self._built = True
    
        
    def rebuild(self, mult=1, vibgen_approx=None):
        """Cleans the object and rebuilds
        
        """
        self.clean()
        self.build(mult=mult, vibgen_approx=vibgen_approx)
        
        
    
    #########################################################################
    #
    #    POST BUILDING METHODS
    #
    ########################################################################       
  
    def get_RWA_suggestion(self):
        """Returns average transition energy 
        
        Average transition energy of the monomer as a suggestion for 
        RWA frequency
        
        """
        
        Nn = self.Nb[1]  # number of monomers
        esum = 0.0
        for i in range(Nn):
            mn = self.monomers[i] 
            omeg = mn.get_energy(1) - mn.get_energy(0)
            esum += omeg

        return esum/Nn
        
    
    def get_RelaxationTensor(self, timeaxis,
                       relaxation_theory=None,
                       time_dependent=False,
                       secular_relaxation=False,
                       relaxation_cutoff_time=None,
                       coupling_cutoff=None,
                       recalculate=True):
        """Returns a relaxation tensor corresponding to the aggregate
        
        
        Returns
        -------
        
        RR : RelaxationTensor
            Relaxation tensor of the aggregate
            
        ham : Hamiltonian
            Hamiltonian corresponding to the aggregate, renormalized by
            the system-bath interaction
            
        """
        
        from ..qm import RedfieldRelaxationTensor
        from ..qm import TDRedfieldRelaxationTensor
        from ..qm import FoersterRelaxationTensor
        from ..qm import TDFoersterRelaxationTensor
        from ..qm import RedfieldFoersterRelaxationTensor
        from ..qm import TDRedfieldFoersterRelaxationTensor
        from ..core.managers import eigenbasis_of

        if self._built:
            ham = self.get_Hamiltonian()
            sbi = self.get_SystemBathInteraction()
        else:
            raise Exception()
        
        #
        # Dictionary of available theories
        #
        theories = dict()
        theories[""] = [""]
        theories["standard_Redfield"] = ["standard_Redfield","stR","Redfield",
                                         "CLME2","QME"]
        theories["standard_Foerster"] = ["standard_Foerster","stF","Foerster"]
        theories["combined_RedfieldFoerster"] = ["combined_RedfieldFoerster",
                                                 "cRF","Redfield-Foerster"]
        #
        # Future
        #
        theories["modified_Redfield"] = ["modifield_Redfield", "mR"]
        theories["noneq_modified_Redfield"] = ["noneq_modified_Redfield", 
                                               "nemR"]
        theories["generalized_Foerster"] = ["generalized_Foerster", "gF", 
                                            "multichromophoric_Foerster"]
        theories["noneq_Foerster"] = ["noneq_Foerster", "neF"]
        theories["combined_WeakStrong"] = ["combined_WeakStrong", "cWS"]

        #if ((not recalculate) and 
        #    (relaxation_theory in theories[self._relaxation_theory])):
        #    return self.RelaxationTensor, self.RelaxationHamiltonian
            
        
        if relaxation_theory in  theories["standard_Redfield"]:
            
            if time_dependent:
                
                # Time dependent standard Refield
            
                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = TDRedfieldRelaxationTensor(ham, sbi, 
                                        cutoff_time=relaxation_cutoff_time)
                    if secular_relaxation:
                        relaxT.secularize() 
                ham.unprotect_basis()                        
                                                
            else:
            
                # Time independent standard Refield
            
                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = RedfieldRelaxationTensor(ham, sbi)
                    if secular_relaxation:
                        relaxT.secularize()
                ham.unprotect_basis()  
                
            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham
            self._has_relaxation_tensor = True
            self._relaxation_theory = "standard_Redfield"
                
            return relaxT, ham
            
        elif relaxation_theory in theories["standard_Foerster"]:
            
            if time_dependent:
                
                # Time dependent standard Foerster               
                relaxT = TDFoersterRelaxationTensor(ham, sbi)
                dat = numpy.zeros((ham.dim,ham.dim),dtype=numpy.float64)
                for i in range(ham.dim):
                    dat[i,i] = ham._data[i,i]
                ham_0 = Hamiltonian(data=dat)
          
            else:
            
                # Time independent standard Foerster
            
                #
                # This is done strictly in site basis
                #
            
                relaxT = FoersterRelaxationTensor(ham, sbi)
                dat = numpy.zeros((ham.dim,ham.dim),dtype=numpy.float64)
                for i in range(ham.dim):
                    dat[i,i] = ham._data[i,i]
                ham_0 = Hamiltonian(data=dat)
                
            # The Hamiltonian for propagation is the one without 
            # resonance coupling         
            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham_0
            self._has_relaxation_tensor = True
            self._relaxation_theory = "standard_Foerster"
            
            return relaxT, ham_0
                
        elif relaxation_theory in theories["combined_RedfieldFoerster"]:
            
            if time_dependent:
                
                # Time dependent combined tensor
                ham.subtract_cutoff_coupling(coupling_cutoff)
                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = \
                             TDRedfieldFoersterRelaxationTensor(ham, sbi,
                                            coupling_cutoff=coupling_cutoff,
                                            cutoff_time=relaxation_cutoff_time)
                    if secular_relaxation:
                        relaxT.secularize()
                ham.unprotect_basis()
                ham.recover_cutoff_coupling()                        
                        
            else:
            
                # Time independent combined tensor           
                ham.subtract_cutoff_coupling(coupling_cutoff)
                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = \
                             RedfieldFoersterRelaxationTensor(ham, sbi,
                                            coupling_cutoff=coupling_cutoff,
                                            cutoff_time=relaxation_cutoff_time)
                    if secular_relaxation:
                        relaxT.secularize()

                    #print("Last line of the context", Manager().get_current_basis())
                #print("Left context", Manager().get_current_basis())
                ham.unprotect_basis()
                ham.recover_cutoff_coupling()

            #
            # create a corresponding propagator
            #
            ham1 = Hamiltonian(data=ham.data.copy())
            ham1.subtract_cutoff_coupling(coupling_cutoff)

            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham1
            self._has_relaxation_tensor = True
            self._relaxation_theory = "combined_RedfieldFoerster"
            
            return relaxT, ham1       
            
        elif relaxation_theory in theories["combined_WeakStrong"]: 
            
            pass
               
        else:
            
            raise Exception("Theory not implemented")
        
      
    def get_ReducedDensityMatrixPropagator(self, timeaxis,
                       relaxation_theory=None,
                       time_dependent=False,
                       secular_relaxation=False, 
                       relaxation_cutoff_time=None,
                       coupling_cutoff=None,
                       recalculate=True):
        """Returns propagator of the density matrix
        
        
        
        """
        
        
        from ..qm import ReducedDensityMatrixPropagator
        from ..core.managers import eigenbasis_of
        
            
        relaxT, ham = self.get_RelaxationTensor(timeaxis,
                       relaxation_theory,
                       time_dependent,
                       secular_relaxation, 
                       relaxation_cutoff_time,
                       coupling_cutoff, recalculate=recalculate)
        
        with eigenbasis_of(ham):
            prop = ReducedDensityMatrixPropagator(timeaxis, ham, relaxT)
            
        
        return prop
        
    #FIXME: There must be a general theory here
    def get_RedfieldRateMatrix(self):
        
        from ..qm import RedfieldRateMatrix
        from ..core.managers import eigenbasis_of
        
        if self._built:
            ham = self.get_Hamiltonian()
            sbi = self.get_SystemBathInteraction()
        else:
            raise Exception()        

        ham.protect_basis()
        with eigenbasis_of(ham):
            RR = RedfieldRateMatrix(ham, sbi)
        ham.unprotect_basis()
        
        return RR
            
    def diagonalize(self):
        """Transforms the Hamiltonian 
           and transition dipole moment into diagonal basis 
           
        """
           
        ee,SS = numpy.linalg.eigh(self.HH)
        
        self.HD = ee
        self.SS = SS
        self.S1 = numpy.linalg.inv(SS)
        
        self.HH = numpy.dot(self.S1,numpy.dot(self.HH,self.SS))
        
        for n in range(3):
            self.DD[:,:,n] = numpy.dot(self.S1,
                               numpy.dot(self.DD[:,:,n],self.SS))
        
        Ntot = self.HH.shape[0]
        dd2 = numpy.zeros((Ntot,Ntot),dtype=numpy.float64)
        for a in range(Ntot):
            for b in range(Ntot):
                dd2[a,b] = numpy.dot(self.DD[a,b,:],self.DD[a,b,:])
        #print(dd2)
        self.D2 = dd2
        self.D2_max = numpy.max(dd2)
        

    def _thermal_population(self, temp=0.0, subtract=None):
        """Thermal populations at temperature temp
        
        Thermal populations calculated from the diagonal elements
        of the Hamiltonian 
        
        """
        
        from ..core.units import kB_intK
        #from ..core.managers import eigenbasis_of
        
        kBT = kB_intK*temp
        
        HH = self.get_Hamiltonian()
        
        if subtract is None:
            subtract = numpy.zeros(HH.dim, dtype=numpy.float64)
        
        rho0 = numpy.zeros((HH.dim,HH.dim),dtype=numpy.complex128)
        if temp == 0.0:
            print("Zero temperature")
            rho0[0,0] = 1.0
        else:
            # FIXME: we assume only single exciton band
            ens = numpy.zeros(HH.dim-1, dtype=numpy.float64)
            #
            #with eigenbasis_of(HH):
            #
            # we specify the basis from outside. This allows to choose 
            # canonical equilibrium in arbitrary basis
            for i in range(HH.dim-1):
                ens[i] = HH.data[i+1,i+1] - subtract[i+1]               
            ne = numpy.exp(-ens/kBT)
            sne = numpy.sum(ne)
            rho0_diag = ne/sne
            rho0[1:,1:] = numpy.diag(rho0_diag)
            
        return rho0
    
    
    def _impulsive_population(self):
        
        rho0 = numpy.zeros((self.Ntot,self.Ntot),dtype=numpy.complex128)
        rho0[0,0] = 1.0
        
        dabs = numpy.sqrt(self.DD[:,:,0]**2 + \
                          self.DD[:,:,1]**2 + self.DD[:,:,2]**2)
                          
        rho0 = numpy.dot(dabs,numpy.dot(rho0,dabs))
        
        
    def get_DensityMatrix(self, condition_type=None,
                                relaxation_theory_limit=None,
                                temperature=0):
        """Returns density matrix according to specified condition
        
        Returs density matrix to be used e.g. as initial condition for
        propagation.
        
        Parameters
        ----------
        
        condition_type : str
            Type of the initial condition. If None, the property rho0 is 
            returned.
            
        relaxation_theory_limits : str
            Type of the relaxation theory limits; applies to 
            `thermal_excited_state` condition type. Possible values are
            `weak_coupling` and `strong_coupling`. We mean the system bath
            coupling. When `weak_coupling` is chosen, the density matrix is
            returned in form of a canonical equilibrium in terms of the
            the exciton basis. For `strong_coupling`, the canonical equilibrium
            is calculated in site basis with site energies striped of
            reorganization energies.
            
        Condition types
        ---------------
        
        thermal_excited_state 
            Thermally equilibriuated excited state
            
        impulsive_excitation
            Excitation by ultrabroad laser pulse
            
        """
        if not self._built:
            raise Exception()
            
        if condition_type is None:
            
            return DensityMatrix(data=self.rho0)
            
        elif condition_type == "impulsive_excitation":
            
            rho0 = self._impulsive_population()
            self.rho0 = rho0
            return DensityMatrix(data=self.rho0)
            
        elif condition_type == "thermal_excited_state":
            
            if relaxation_theory_limit is not None:
                
                if relaxation_theory_limit == "strong_coupling":
                    
                    # we need to subtract reorganization energies
                    Ndim = self.get_Hamiltonian().dim
                    re = numpy.zeros(Ndim, dtype=numpy.float64)
                    for i in range(1, Ndim):
                        # FIXME: fix the access to reorganization energy in SBI
                        re[i] = self.sbi.CC.get_reorganization_energy(i-1,i-1)
                        #print(i, re[i]/cm2int)
                    rho0 = self._thermal_population(temperature, subtract=re)
                    
                elif relaxation_theory_limit == "weak_coupling":
                    
                    rho0 = self._thermal_population(temperature)
                    
                else:
                    raise Exception("Unknown relaxation_theory_limit")
            else:
                rho0 = self._thermal_population(temperature)
                
            self.rho0 = rho0
            return DensityMatrix(data=self.rho0)
            
        else:
            raise Exception("Unknown condition type")
        
        
    def get_electronic_groundstate(self):
        """Indices of states in electronic ground state
        
        
        Returns indices of all states in the electronic
        ground state of the system.
        
        """
           
        Ng = self.Nb[0]
        lst = [k for k in range(Ng)]
           
        return tuple(lst)
        
    
    def get_excitonic_band(self, band=1):
        """Indices of states in a given excitonic band.
        
        
        Returns indices of all states in the excitonic band 
        with number of excitons equal to `band` 
        
        Parameters
        ----------

        band : int
            Specifies which band should be returned.
            
        """ 
        Nbefore = 0
        for ii in range(band):       
            Nbefore += self.Nb[ii]
        Nin = self.Nb[band]
        lst = [k for k in range(Nbefore,Nbefore+Nin)]
        
        return tuple(lst)
        
    def get_transition(self,Nf,Ni):
        """Returns relevant info about the energetic transition
        
        Parameters
        ----------

        Nf : int
            Final state of the transition
            
        Ni : int
            Initial state of the transition
        
        """
        
        energy = self.HH[Nf,Nf]-self.HH[Ni,Ni]
        trdipm = self.DD[Nf,Ni,:]
        
        return (energy,trdipm)
        
    def get_SystemBathInteraction(self):
        return self.sbi
        
    def get_Hamiltonian(self):
        if self._built:
            return self.HamOp #Hamiltonian(data=self.HH) 
        else:
            raise Exception("Aggregate object not built")
            

    def get_TransitionDipoleMoment(self):
        if self._built:
            return TransitionDipoleMoment(data=self.DD)                     
        else:
            raise Exception("Aggregate object not built")
            
            
            
    ########################################################################
    #
    #   SPECTROSCOPY
    #
    ########################################################################
                       
    def liouville_pathways_3(self,ptype="R3g",dtol=-1.0,ptol=1.0e-3,lab=None):
        """ Generator of Liouville pathways """
        
        pop_tol = ptol
        dip_tol = numpy.sqrt(self.D2_max)*dtol
        
        # Check if the ptype is a tuple
        if not isinstance(ptype, (tuple,list)):
            ptype_tuple = (ptype,)
        else:
            ptype_tuple = ptype
        lst = []
         
        for ptp in ptype_tuple:
        
            if ptp == "R3g":
            
                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:

                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break
                            
                            for i3g in ngs:
                                
                                if self.D2[i3g,i2e] < dip_tol:
                                    break
                                
                                for i4e in nes:
                            
                                    if ((self.D2[i4e,i1g] < dip_tol)
                                    and (self.D2[i3g,i4e] < dip_tol)) :
                                        break
                                   
                                    l += 1

                                    #      Diagram R3g
                                    #
                                    #                                     
                                    #      |g_i3> <g_i3|
                                    # <----|-----------|
                                    #      |e_i4> <g_i3|
                                    # ---->|-----------|
                                    #      |g_i1> <g_i3|
                                    #      |-----------|---->
                                    #      |g_i1> <e_i2|
                                    #      |-----------|<----
                                    #      |g_i1> <g_i1|
                                    
                                    try:

                                        lp = \
                                        diag.liouville_pathway("R", i1g,
                                               aggregate=self,
                                               order=3,pname=ptp)         
                                        # |g_i1> <g_i1|
                                        lp.add_transition((i2e,i1g),-1)
                                        # |g_i1> <e_i2|
                                        lp.add_transition((i3g,i2e),-1)
                                        # |g_i1> <g_i3|
                                        lp.add_transition((i4e,i1g),+1)
                                        # |e_i5> <g_i3|
                                        lp.add_transition((i3g,i4e),+1)
                                        # |g_i3> <g_i3|

                                    except:
                                        
                                        
                                        break
                                    
                                    lp.build()
                                    lst.append(lp)
                                    k += 1
            
            if ptp == "R2g":

                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break
                            
                            for i3e in nes:
                                
                                if self.D2[i3e,i1g] < dip_tol:
                                    break
                                
                                for i4g in ngs:

                                    if ((self.D2[i4g,i2e] < dip_tol)
                                     or (self.D2[i4g,i3e] < dip_tol)):
                                        break
                                    
                                    l += 1

                                    #      Diagram R2g
                                    #
                                    #                                     
                                    #      |g_i4> <g_i4|
                                    # <----|-----------|
                                    #      |e_i3> <g_i4|
                                    #      |-----------|---->
                                    #      |e_i3> <e_i2|
                                    # ---->|-----------|
                                    #      |g_i1> <e_i2|
                                    #      |-----------|<----
                                    #      |g_i1> <g_i1|
                                    
                                    try:
                                        lp = \
                                        diag.liouville_pathway("R", i1g,
                                                           aggregate=self,
                                                           order=3,pname=ptp,
                                                           popt_band=1)
                                        #      |g_i1> <g_i1|
                                        lp.add_transition((i2e,i1g),-1)
                                        #      |g_i1> <e_i2|
                                        lp.add_transition((i3e,i1g),+1)
                                        #      |e_i3> <e_i2|
                                        lp.add_transition((i4g,i2e),-1)
                                        #      |e_i3> <g_i4|
                                        lp.add_transition((i4g,i3e),+1)
                                        #      |g_i4> <g_i4|

                                    except:
                                        
                                        break
                                    
                                    lp.build()
                                    lst.append(lp)
                                    k += 1
                
             
            if ptp == "R1g":
                
                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                #nrg = len(ngs)
                #nre = len(nes) 
                
                #print("Ground state : ", nrg)
                #print("Excited state: ", nre)
                #print("R1g: ",nrg*nre*nre*nrg)
                
                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break

                            for i3e in nes:

                                if self.D2[i3e,i1g] < dip_tol:
                                    break

                                for i4g in ngs:

                                    if ((self.D2[i4g,i3e] < dip_tol)
                                     or (self.D2[i4g,i2e] < dip_tol)):
                                        break

                                    l += 1

                                    #      Diagram R1g
                                    #
                                    #                                     
                                    #      |g_i4> <g_i4|
                                    # <----|-----------|
                                    #      |e_i2> <g_i4|
                                    #      |-----------|---->
                                    #      |e_i2> <e_i3|
                                    #      |-----------|<----
                                    #      |e_i2> <g_i1|
                                    # ---->|-----------|
                                    #      |g_i1> <g_i1|
                                
                                    try:
                                        lp = \
                                        diag.liouville_pathway("NR",i1g,
                                                           aggregate=self,
                                                           order=3,pname=ptp,
                                                           popt_band=1)
                                        #      |g_i1> <g_i1|                                                           
                                        lp.add_transition((i2e,i1g),+1)
                                        #      |e_i2> <g_i1|        
                                        lp.add_transition((i3e,i1g),-1)
                                        #      |e_i2> <e_i3|
                                        lp.add_transition((i4g,i3e),-1)
                                        #      |e_i2> <g_i4|
                                        lp.add_transition((i4g,i2e),+1)
                                        #      |g_i4> <g_i4|

                                    except:
                                        
                                        break
                                    
                                    lp.build()
                                    lst.append(lp)
                                    k += 1
            
            if ptp == "R4g":
                
                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                #nrg = len(ngs)
                #nre = len(nes) 
                
                #print("Ground state : ", nrg)
                #print("Excited state: ", nre)
                #print("R4g: ",nrg*nre*nrg*nrg*nre)
                
                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break
                            
                            for i3g in ngs:

                                if self.D2[i3g,i2e] < dip_tol:
                                    break
                                
                                for i4e in nes:

                                    if ((self.D2[i4e,i3g] < dip_tol)
                                     or (self.D2[i1g,i4e] < dip_tol)):
                                        break
                                    
                                    l += 1
                                    

                                    #      Diagram R4g
                                    #
                                    #                                     
                                    #      |g_i1> <g_i1|
                                    # <----|-----------|
                                    #      |e_i4> <g_i1|
                                    # ---->|-----------|
                                    #      |g_i3> <g_i1|
                                    # <----|-----------|
                                    #      |e_i2> <g_i1|
                                    # ---->|-----------|
                                    #      |g_i1> <g_i1|

                                    try:
                                        lp = \
                                        diag.liouville_pathway("NR",i1g,
                                                           aggregate=self,
                                                           order=3,pname=ptp)
                                        #      |g_i1> <g_i1|                                                           
                                        lp.add_transition((i2e,i1g),+1)
                                        #      |e_i2> <g_i1|
                                        lp.add_transition((i3g,i2e),+1)
                                        #      |g_i3> <g_i1|
                                        lp.add_transition((i4e,i3g),+1)
                                        #      |e_i4> <g_i1|
                                        lp.add_transition((i1g,i4e),+1)
                                        #      |g_i1> <g_i1|

                                    except:
                                        
                                        break
                                    
                                    lp.build()
                                    lst.append(lp)
                                    k += 1
            
            if ptp == "R1f*":
                
                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                try:
                    nfs = self.get_excitonic_band(band=2)
                except:
                    break
                
#                print(ngs)
#                print(nes)
#                print(nfs)
#                for a in nes:
#                    for b in nfs:
#                        print(a,b," : ",self.D2[a,b],self.D2[b,a])

                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break
                            
                            for i3e in nes:
                                
                                if self.D2[i3e,i1g] < dip_tol:
                                    break
                                
                                for i4f in nfs:

                                    if ((self.D2[i4f,i3e] < dip_tol)
                                     or (self.D2[i2e,i4f] < dip_tol)):
                                        #print("Breaking")
                                        #print(self.D2[i4f,i3e],self.D2[i2e,i4f])
                                        break
                                    
                                    l += 1
                                    

                                    #      Diagram R4g
                                    #
                                    #                                     
                                    #      |e_i2> <e_i2|
                                    # <----|-----------|
                                    #      |f_i4> <e_i2|
                                    # ---->|-----------|
                                    #      |e_i3> <e_i2|
                                    # ---->|-----------|
                                    #      |g_i1> <e_i2|
                                    #      |-----------|<----
                                    #      |g_i1> <g_i1|

                                    try:

                                        lp = \
                                        diag.liouville_pathway("R",i1g,
                                                           aggregate=self,
                                                           order=3,pname=ptp,
                                                           popt_band=1)
                                        #      |g_i1> <g_i1|                                                           
                                        lp.add_transition((i2e,i1g),-1)
                                        #      |g_i1> <e_i2|
                                        lp.add_transition((i3e,i1g),+1)
                                        #      |e_i3> <e_i2|
                                        lp.add_transition((i4f,i3e),+1)
                                        #      |f_i4> <e_i2|
                                        lp.add_transition((i2e,i4f),+1)
                                        #      |e_i2> <e_i2|

                                    except:
                                        
                                        break
                                    
                                    lp.build()
                                    lst.append(lp)
                                    k += 1
            
            if ptp == "R2f*":
                
                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                try:
                    nfs = self.get_excitonic_band(band=2)
                except:
                    break
                

                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break                                                        
                            
                            for i3e in nes:
                                
                                if self.D2[i3e,i1g] < dip_tol:
                                    break

                                for i4f in nfs:

                                    if ((self.D2[i4f,i2e] < dip_tol)
                                     or (self.D2[i3e,i4f] < dip_tol)):
                                        break
                                    
                                    l += 1
                                    

                                    #      Diagram R4g
                                    #
                                    #                                     
                                    #      |e_i3> <e_i3|
                                    # <----|-----------|
                                    #      |f_i4> <e_i3|
                                    # ---->|-----------|
                                    #      |e_i2> <e_i3|
                                    #      |-----------|<----
                                    #      |e_i2> <g_i1|
                                    # ---->|-----------|
                                    #      |g_i1> <g_i1|

                                    try:

                                        lp = \
                                        diag.liouville_pathway("NR",i1g,
                                                           aggregate=self,
                                                           order=3,pname=ptp,
                                                           popt_band=1)
                                        #      |g_i1> <g_i1|                                                           
                                        lp.add_transition((i2e,i1g),+1)
                                        #      |e_i2> <g_i1|
                                        lp.add_transition((i3e,i1g),-1)
                                        #      |e_i2> <e_i3|
                                        lp.add_transition((i4f,i2e),+1)
                                        #      |f_i4> <e_i3|
                                        lp.add_transition((i3e,i4f),+1)
                                        #      |e_i3> <e_i3|

                                    except:
                                        
                                        break
                                    
                                    lp.build()
                                    lst.append(lp)
                                    k += 1
                    

            if ptp == "R2g->3g":

                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break
                            
                            for i3e in nes:
                                
                                if self.D2[i3e,i1g] < dip_tol:
                                    break
                                
                                # relaxation 
                                for i4g in ngs:
                                    for i5g in ngs:
                                
                                        for i6e in nes:

                                            if ((self.D2[i6e,i4g] < dip_tol)
                                            or (self.D2[i5g,i6e] < dip_tol)):
                                                break
                                    
                                            l += 1

                                    #      Diagram R2g_ETICS
                                    #      (Compensates R3g)
                                    #
                                    #                                     
                                    #      |g_i5> <g_i5|
                                    # <----|-----------|
                                    #      |e_i6> <g_i5|
                                    # ---->|-----------|
                                    #      |g_i4> <g_i5|
                                    #      |***********|
                                    #      |e_i3> <e_i2|
                                    # ---->|-----------|
                                    #      |g_i1> <e_i2|
                                    #      |-----------|<----
                                    #      |g_i1> <g_i1|
                                    
                                            if True:
                                            #try:
                                                lp = \
                                                diag.liouville_pathway("R_E",
                                                           i1g,
                                                           aggregate=self,
                                                           order=3,
                                                           relax_order=1,
                                                           pname=ptp)
                                                #      |g_i1> <g_i1|
                                                lp.add_transition((i2e,i1g),-1)
                                                #      |g_i1> <e_i2|
                                                lp.add_transition((i3e,i1g),+1)
                                                #      |e_i3> <e_i2|
                                                lp.add_transfer((i4g,i5g),
                                                                  (i3e,i2e))
                                                #      |g_i4> <g_i5|
                                                lp.add_transition((i6e,i4g),+1)
                                                #      |e_i6> <g_i5|
                                                lp.add_transition((i5g,i6e),+1)
                                                #      |g_i5> <g_i5|

                                            #except:
                                        
                                            #    break
                                    
                                            lp.build()
                                            lst.append(lp)
                                            k += 1

            if ptp == "R1g->4g":

                ngs = self.get_electronic_groundstate()
                nes = self.get_excitonic_band(band=1)
                
                k = 0
                l = 0
                for i1g in ngs:
                    
                    # Only thermally allowed starting states are considered
                    if self.rho0[i1g] > pop_tol:
                
                        for i2e in nes:
                            
                            if self.D2[i2e,i1g] < dip_tol:
                                break
                            
                            for i3e in nes:
                                
                                if self.D2[i3e,i1g] < dip_tol:
                                    break
                                
                                # relaxation 
                                for i4g in ngs:
                                    for i5g in ngs:
                                
                                        for i6e in nes:

                                            if ((self.D2[i6e,i4g] < dip_tol)
                                            or (self.D2[i5g,i6e] < dip_tol)):
                                                break
                                    
                                            l += 1

                                    #      Diagram R2g_ETICS
                                    #      (Compensates R3g)
                                    #
                                    #                                     
                                    #      |g_i5> <g_i5|
                                    # <----|-----------|
                                    #      |e_i6> <g_i5|
                                    # ---->|-----------|
                                    #      |g_i4> <g_i5|
                                    #      |***********|
                                    #      |e_i2> <e_i3|
                                    #      |-----------|<----
                                    #      |e_i2> <g_i1|
                                    # ---->|-----------|
                                    #      |g_i1> <g_i1|
                                    
                                            #if True:
                                            try:
                                                lp = \
                                                diag.liouville_pathway("NR_E",
                                                           i1g,
                                                           aggregate=self,
                                                           order=3,
                                                           relax_order=1,
                                                           pname=ptp)
                                                #      |g_i1> <g_i1|
                                                lp.add_transition((i2e,i1g),+1)
                                                #      |e_i2> <g_i1|
                                                lp.add_transition((i3e,i1g),-1)
                                                #      |e_i2> <e_i3|
                                                lp.add_transfer((i4g,i5g),
                                                                  (i2e,i3e))
                                                #      |g_i4> <g_i5|
                                                lp.add_transition((i6e,i4g),+1)
                                                #      |e_i6> <g_i5|
                                                lp.add_transition((i5g,i6e),+1)
                                                #      |g_i5> <g_i5|

                                            except:
                                        
                                                break
                                    
                                            lp.build()
                                            lst.append(lp)
                                            k += 1

         
        if lab is not None:
            for l in lst:
                l.orientational_averaging(lab)
         
        return lst     
        
    
    def ETICS_evolution_operator(self,popt,K,proj):
        """ETICS evolution operator
        
        Parameters
        ----------
        
        popt : float
            Population time
            
        K : float
            Relaxation rate
            
        proj : array
            An array of electronic states representing a projector
            on the state which
            gets deexcited in the process of ETICS
            
        """
        
        # all this uses site basis        
            
        
        # this is the evolution superoperator at time popt
        U_ETICS = numpy.zeros((self.Nb[0],self.Nb[0],
                               self.Nb[1],self.Nb[1]),dtype=numpy.complex128)
        U_EX    = numpy.zeros((self.Nb[1],self.Nb[1]),dtype=numpy.complex128)
                               
        
        # FC factors and diagonalization 
        Ceg = numpy.zeros((self.Nb[1],self.Nb[0]))
        Cge = numpy.zeros((self.Nb[0],self.Nb[1]))
        
        # Cge
        if len(proj)>1:
            raise Exception("Not implemented yet")            
        a = proj[0]
        
        esg = self.get_electronic_state(self.elsigs[0])
        ag = 0
        for vg in esg.vsignatures():
            vs_g = vibronic_state(esg,vg)
            ae = 0
            for ie in range(1,self.number_of_electronic_states_in_band(1)+1):
                ese = self.get_electronic_state(self.elsigs[ie])
                for ve in ese.vsignatures():
                    vs_e = vibronic_state(ese,ve)
                    if True:
                    #if ie == a:
                        Cge[ag,ae] = self.fc_factor(vs_g,vs_e)
                    else:
                        Cge[ag,ae] = 0.0
                    ae += 1
            ag += 1
        
        
        # we use the fact that we are diagonalized
        S1 = self.S1
        
        Cge = numpy.dot(Cge,S1[self.Nb[0]:(self.Nb[0]+self.Nb[1]),
                               self.Nb[0]:(self.Nb[0]+self.Nb[1])])
                               
        # Ceg
        Ceg = Cge.T 
        
        # frequencies between states in the ground and excited state 
        omegas_g = numpy.zeros((self.Nb[0],self.Nb[0]),dtype=numpy.float64)
        omegas_e = numpy.zeros((self.Nb[1],self.Nb[1]),dtype=numpy.float64)
        for a in range(self.Nb[0]):
            for b in range(self.Nb[0]):
                omegas_g[a,b] = self.HH[a,a]-self.HH[b,b]
                
        for a in range(self.Nb[0],self.Nb[0]+self.Nb[1]):
            for b in range(self.Nb[0],self.Nb[0]+self.Nb[1]):
                omegas_e[a-self.Nb[0],b-self.Nb[0]] = self.HH[a,a]-self.HH[b,b]
                        
        
        # some precalculated values
        eom_me = numpy.exp(-1j*popt*omegas_e)
        eom_mg = numpy.exp(-1j*popt*omegas_g)
        eom_pg = numpy.exp( 1j*popt*omegas_g)



        KK = numpy.zeros((self.Nb[0],self.Nb[0],
                               self.Nb[1],self.Nb[1]),dtype=numpy.float64)

        for ag in range(self.Nb[0]):
            for bg in range(self.Nb[0]):
                for ae in range(self.Nb[1]):
                    for be in range(self.Nb[1]):
                        KK[ag,bg,ae,be] = K*Cge[ag,ae]*Ceg[be,bg]
                        
        eK = numpy.exp(-0.5*K*popt)   


        for ag in range(self.Nb[0]):
            for bg in range(self.Nb[0]):
                for ae in range(self.Nb[1]):
                    for be in range(self.Nb[1]):
                        
                        U_ETICS[ag,bg,ae,be] = KK[ag,bg,ae,be] \
                *(((KK[ag,bg,ae,be]+1j*(omegas_g[ag,bg]-omegas_e[ae,be]))/
                (KK[ag,bg,ae,be]**2 + (omegas_g[ag,bg]-omegas_e[ae,be])**2))
                *eom_mg[ag,bg]) \
                *(1.0-eom_pg[ag,bg]*eom_me[ae,be]*(eK**2))
                
                        if (abs(omegas_g[ag,bg] - omegas_e[ae,be])>1.0*cm2int):
                            U_ETICS[ag,bg,ae,be] = 0.0
                        #print(">",ag,bg,ae,be,"->",U_ETICS[ag,bg,ae,be])

        for ae in range(self.Nb[1]):
            for be in range(self.Nb[1]):
                if ae != be:
                    U_EX[ae,be] = numpy.exp(-0.5*K*popt)*eom_me[ae,be]
        for ae in range(self.Nb[1]):
            U_EX[ae,ae] = numpy.exp(-K*popt)                         
        
        # we return a result in exciton basis
        return U_ETICS, U_EX
        
        
        

        
        
        
