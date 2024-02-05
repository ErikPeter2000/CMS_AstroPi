import math

def standardDeviation(values):
    """
    Calculate the standard deviation of a list of values.
    """
    mean = sum(values) / len(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))

def standardDeviationAngles(values):
    """
    Calculate the standard deviation of a list of angles.
    """
    mean = sum(values) / len(values)
    return math.sqrt(sum((math.sin(x - mean) ** 2 for x in values) / len(values)))

def weightedMean(values, weights):
    """
    Calculate the weighted mean of a list of values.
    """
    return sum(values[i] * weights[i] for i in range(len(values))) / sum(weights)

def weightedMeanPairs(values):
    """
    Calculate the weighted mean of a list of pairs of values.
    """
    return (weightedMean([v[0] for v in values], [v[1] for v in values]), weightedMean([v[1] for v in values], [v[0] for v in values]))

def mean(values):
    return sum(values) / len(values)