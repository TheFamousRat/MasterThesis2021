import scipy
import numpy as np

from sklearn.metrics.pairwise import pairwise_kernels

class LowRankRecovery:
    def __init__(self):
        #Optimizitation params
        self.w = 0.5                         #Base learning rate
        self.c = 1.2                         #Learning rate multiplicative increase
        self.lambd0 = 0.5                    #Base error matrix norm weight
        self.itersMax = 100                  #Max number of iterations
        self.eps = 1e-4                      #Convergence criteria
        #Kernel params
        self.sigma = 5.0                     #Kernel parameters (the following are for computation convenience)
        self.sigmaSq = self.sigma**2
        self.gamma = 1.0/(2.0 * self.sigmaSq)

    def getKernelMat(self, X):
        """
        Computes the kernel matrix of a given data matrix
        """
        return pairwise_kernels(X.T, metric = 'rbf', gamma = self.gamma)

    def softThresholdMat(self, X, thres):
        """
        Applies to each element of a matrix the function f(x) = sign(x) * max(0, abs(x) - thres)
        """
        A = np.abs(X) - thres
        return np.sign(X) * np.multiply(A, A > 0.0)

    def getStepSizeAndGradient(self, gLgK, K, X):
        """
        Computes the step size and the loss gradient wrt E 
        """
        H = np.multiply(gLgK, K)
        BH = np.ones(X.shape) @ H
        I = np.identity(H.shape[0])
        
        g = -(2.0/self.sigmaSq)*(X @ H - np.multiply(X, BH))
        
        stepSize = self.w * np.linalg.norm((2.0/self.sigmaSq)*(H-I*np.average(BH)), ord = 2)
        return g, stepSize

    def recoverLowRank(self, M):
        """
        Recovering a low-rank matrix by the RKPCA algorithm (PLM version). Code adapted from https://github.com/jicongfan/RKPCA_TNNLS2019
        """
        #Matrices to recover : E is the sparse error matrix, X is the "noise-free" matrix
        E = np.zeros(M.shape)
        X = M - E
        #Constants
        I = np.identity(M.shape[1]) #Identity matrix
        normM = np.sum(np.abs(M)) #1-norm of the input matrix
        lambd = M.shape[1] * self.lambd0 / normM #Weight given to the error norm

        iterNum = 0
        prevCost = float('inf')
        while iterNum < self.itersMax:
            iterNum += 1
            ##One step beginning
            #Kernel matrix computations
            K = self.getKernelMat(X)
            Ksqrt = scipy.linalg.sqrtm(K)
            
            #Gradient computation
            gLgK = 0.5 * scipy.linalg.inv(Ksqrt)# @ scipy.linalg.inv(K + I*1e-5))
            gE, stepSize = self.getStepSizeAndGradient(gLgK, K, X)
            
            #Updating E (and X)
            prevE = np.copy(E)
            E = self.softThresholdMat(E - gE / stepSize, lambd / stepSize)
            X = M - E
            
            #Updating the learning rate's scale
            newCost = np.trace(Ksqrt) + lambd * np.sum(np.abs(E)) 
            if newCost > prevCost:
                self.w = min(5.0, self.w * self.c)
            prevCost = newCost
            
            #Convergence condition checking
            if np.linalg.norm(E - prevE) / normM < self.eps:
                break

        return E