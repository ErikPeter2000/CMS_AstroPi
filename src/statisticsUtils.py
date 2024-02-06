# Utility functions for calculating means and deviations.

import math
import numpy as np

def standardDeviation(values):
    """Calculate the standard deviation of a list of values."""
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))

def standardDeviationAngles(values):
    """Calculate the standard deviation of a list of angles."""
    mean = sum(values) / len(values)
    return math.sqrt(sum((math.sin(x - mean) ** 2) for x in values) / len(values))

def weightedMean(values, weights):
    """Calculate the weighted mean of a list of values."""
    return sum(values[i] * weights[i] for i in range(len(values))) / sum(weights)

def weightedMeanPairs(values):
    """Calculate the weighted mean of a list of pairs of values."""
    return weightedMean([v[0] for v in values], [v[1] for v in values])

def weightedMeanPairsWithDiscard(pairs, percentile):
    """Calculate the weighted mean of a list of pairs of values, discarding outliers."""
    newPairs = discardOutliers(pairs, percentile)
    return weightedMeanPairs(newPairs if len(newPairs) > 0 else pairs)

def meanAndDeviation(values):
    """Calculate the mean and standard deviation of a list of values."""
    mean = sum(values) / len(values)
    return (mean, math.sqrt(sum((x - mean) ** 2 for x in values) / len(values)))

def meanAndDeviationAngles(values):
    """Calculate the mean and standard deviation of a list of angles."""
    mean = sum(values) / len(values)
    return (mean, math.sqrt(sum((math.sin(x - mean) ** 2 for x in values) / len(values))))

def discardOutliers(pairs, percentile):
    """Discards outlier pairs from a list, based on the given percentile.
    E.g: A percentile of 5 will discard the top and bottom 5% of the list."""
    # assume values are uniformly distributed and discard outliers
    # Calculate the value at each percentiles
    values = [i[0] for i in pairs]
    max = np.percentile(values, 100 - percentile)
    min = np.percentile(values, percentile)
    
    # Filter the list to only include with the given range
    filtered_values = filter(lambda x: x[0] <= max and x[0] >= min, pairs)
    return list(filtered_values)

def mean(values):
    return sum(values) / len(values)