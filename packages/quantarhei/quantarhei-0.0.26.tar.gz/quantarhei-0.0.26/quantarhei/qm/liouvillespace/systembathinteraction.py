# -*- coding: utf-8 -*-
"""
    Quantarhei package (http://www.github.com/quantarhei)

    systembathinteraction module

"""
import numpy

from ...core.saveable import Saveable
from ...qm.corfunctions.cfmatrix import CorrelationFunctionMatrix

class SystemBathInteraction(Saveable):
    """Describes interaction of an open quantum system with its environment
    
    Stores the system--bath interaction operator in form of a set of operators
    on the Hilbert space of the system and correlation functions of 
    the operator on the bath Hilbert space.
    
    Parameters
    ----------
    
    sys_operators : list
        List of the system part of the system-bath interaction Hamiltonian
        components
    
    bath_correlation_matrix: CorrelationFunctionMatrix 
        Object of the CorrelationFunctionMatrix type holding all correlation
        functions needed for the description of system bath interaction
    
    
    """

    def __init__(self, sys_operators=None, bath_correlation_matrix=None,
                 system=None):

        if ((sys_operators is not None) 
            and (bath_correlation_matrix is not None)):
            # Find the length of the list of operators 
            if isinstance(sys_operators,list):
                self.N = len(sys_operators)
            else:
                raise Exception("First argument has to a list")
            
            # Second argument has to be a CorrelationFunctionMatrix 
            if not isinstance(bath_correlation_matrix, CorrelationFunctionMatrix):
                raise Exception("Second argument has to a"+
                                " CorrelationFunctionMatrix")
                
            # Check that sys_operators and bath_correlation matrix has 
            # a compatible number of components
            if bath_correlation_matrix.nob != self.N:
                raise Exception("Incompatile number of bath compoments: " +
                    ("Correlation function matrix - %i vs. operators %i" % 
                    (bath_correlation_matrix.nob,self.N)))
                
            self.TimeAxis = bath_correlation_matrix.timeAxis
            
            # information about aggregate is needed when dealing with 
            # multiple excitons
            self.aggregate = None
            self.molecule = None
            self.system = None
    
            from ...builders.aggregates import Aggregate
            from ...builders.molecules import Molecule    
            
            if system is not None:
                if isinstance(system, Aggregate):
                    self.aggregate = system
                    self.molecule = None
                    self.system = self.aggregate
    
                if isinstance(system, Molecule):
                    self.aggregate = None
                    self.molecule = system
                    self.system = self.molecule
    
                
            if self.N > 0:
                
                # First of the operators 
                KK = sys_operators[0]
            
                # Get its dimension 
                dim = KK.data.shape[0]
            
                # Test if it is really an Operator and if yes then save it
                if True:
                    
                    self.KK = numpy.zeros((self.N, dim, dim), dtype=numpy.float64)
                    self.KK[0,:,:] = KK.data       
                
                # Save other operators and check their dimensions 
                for ii in range(1,self.N):
                    
                    KK = sys_operators[ii]
                    
                    if True: #isinstance(KK,Operator):
                        if dim == KK.data.shape[0]:
                            self.KK[ii,:,:] = KK.data
                        else:
                            raise Exception("Operators in the list are" 
                            + " not of the same dimension")
                    else:
                        raise Exception("sys_operators tuple (the first argument)"
                        + " has to contain cu.oqs.hilbertspace.Operator")
                    
                self.CC = bath_correlation_matrix
                
            else:
                
                self.KK = None
                self.CC = None
                      
    # FIXME: Better get rid of the dependence on the upstream operator 
    def _before_save(self):
        
        self._S__aggregate = self.aggregate
        self._S__system = self.system
        self.aggregate = None
        self.system = None
        
    def _after_save(self):
        self.aggregate = self._S__aggregate
        self.system = self._S__system
        
    def _after_load(self):
        
        pass
        
    def get_coft(self,n,m):
        """Returns bath correlation function corresponding to sites n and m

        
        """
        if self.system is None:
            
            return self.CC.get_coft(n,m)
            
        else:
            
            bn = self.system.which_band[n]
            bm = self.system.which_band[m]
            
            if ((bn == 0) and (bm == 0)):
                
                #print(bn,"::",n,m)
                return self.CC._cofts[0,:]
                
            elif ((bn == 1) and (bm == 1)):
                #print(bn,"::",n-1,m-1)
                
                return self.CC.get_coft(n-1,m-1)
                
            else:
                
                return self.CC._cofts[0,:]
                
                
                
    def get_coft_elsig(self,n_sig,m_sig):
        """Returns bath correlation based on electronic signatures 


        """ 
                 
        nb = numpy.sum(n_sig)
        mb = numpy.sum(m_sig)
        
        indices = []
        if mb == nb:
            ni = 0
            for na in n_sig:
                mi = 0
                for ma in m_sig:
                    if ((na == 1) and (ma == 1)):
                        indices.append([ni,mi]) 
                    mi += 1
                ni += 1
            
            ret = numpy.zeros((self.TimeAxis.length),dtype=numpy.complex128)
            for ind in indices:
                #print(nb,":",ind[0],ind[1])
                ret += self.get_coft(ind[0],ind[1]) 
                    
                
            return ret            
            
        else:
            return self.CC._cofts[0,:]
