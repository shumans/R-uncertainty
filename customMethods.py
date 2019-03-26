#Defining methods for MonteCarloModeling

import numpy as np
import numpy.random as npRand
import scipy.stats as stats

#MultiDimensional numpy linspace
def ndlinspace(start, end, steps):
    if (start.shape != end.shape):
        print("Arrays must be same size")
        return
    if (start.ndim == 1):
        result = np.array(
            [np.linspace(s, e, steps) for s,e in zip(start, end)]
        )
        return result
    result = np.array(
        [ndlinspace(s, e, steps) for s,e in zip(start, end)]
    )
    return result

#choosing random data sets for each star type
def ndNormalData(mean, sigma, numVals):
    if (mean.shape != sigma.shape):
        print("Arrays must be same size")
        return
    if (mean.ndim == 1):
        data = np.array(
            [npRand.normal(m, s, numVals) for m, s in zip(mean, sigma)]
        )
        return data
    
    data = np.array(
        [ndNormalData(m, s, numVals) for m, s in zip(mean, sigma)]
    )
    return data

#Defines binning of data to evenly space bins close to the mean
#and group the outer bins together. This avoids an expected bincount of 0
#for calculating chi-squared.
def customBinning(data, numBins=20, dataWidth=7):
    low = dataMin = min(data)
    high = dataMax = max(data)
    mean = np.mean(data)
    stdev = np.std(data)
    
    if (dataMin < mean - dataWidth * stdev):
        numBins = numBins - 1
        low = mean - dataWidth * stdev
    if (dataMax > mean + dataWidth * stdev):
        numBins = numBins - 1
        high = mean + dataWidth * stdev
    
    bins = np.linspace(low, high, numBins + 1)
    
    if (dataMin != low):
        bins = np.concatenate((dataMin, bins), axis = None)
    if (dataMax != high):
        bins = np.concatenate((bins, dataMax), axis = None)
    
    return bins

def ndHistogramCounts(Vals, numBins):
    if (Vals.ndim == 1):
        bins = customBinning(Vals, numBins)
        counts, Bins = np.histogram(Vals, bins)
        return counts
    
    results = np.stack(
        ndHistogramCounts(vals, numBins) for vals in Vals
    )
    
    return results

def ndHistogramBins(Vals, numBins):
    if (Vals.ndim == 1):
        bins = customBinning(Vals, numBins)
        #counts, Bins = np.histogram(Vals, bins)
        return bins
    
    results = np.stack(
        ndHistogramBins(vals, numBins) for vals in Vals
    )
    
    return results

def ndNormalCounts(mean, sigma, Bins):
    if (mean.shape != sigma.shape):
        print("Arrays must be same shape")
        return
    
    if (mean.ndim == 1):
        counts = np.diff(np.stack(
            stats.norm.cdf(bins, m, s) for bins, m, s in zip(Bins, mean, sigma)
        ))
        return counts
    
    counts = np.stack(
        ndNormalCounts(m, s, bins) for m, s, bins in zip(mean, sigma, Bins)
    )
    return counts

#For interactive color selection
def f(color1):
	return color1
def g(color2):
	return color2