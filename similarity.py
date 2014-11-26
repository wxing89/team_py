import math

jaccardMax = 1
jaccardMin = 0

def normalSimilarity(s1, s2):
    """
    """
    try:
        return len(s1 & s2) / math.sqrt(float(len(s1) ** 2 + len(s2) ** 2))
    except ZeroDivisionError:
        return 1


def jaccardIndex(s1, s2):
    """Compute the Jaccard index between the two sample sets 's1' and 's2'.

    The return value is a float between 0 and 1, where 0 means totally different, and 1 equal.
    """
    try:
        return len(s1 & s2) / float(len(s1 | s2))
    except ZeroDivisionError:
        return 1
    except TypeError:
        set1, set2 = set(s1), set(s2)
        return jaccardIndex(set1, set2)


def jaccardDistance(s1, s2):
    """Compute the Jaccard distance between the two sample sets 's1' and 's2'.

    The return value is a float between 0 and 1, where 0 means equal, and 1 totally different.
    """
    return 1 - jaccardIndex(s1, s2)



def cosineSimilarity(s1, s2):
    """Compute the Cosine Similarity between the two sample set 's1' and 's2'.

    The return value is a float between 0 and 1, where 0 means totally different, and 1 equal.
    """
    return len(s1 & s2) / math.sqrt(float(len(s1) * len(s2)))


def cosineSimImproved(s1, s2):
    l1, l2 = len(s1), len(s2)
    m = len(s1 & s2)
    n = len(s1 | s2)
    return (1 - l1 / n) * (1 - l2 / n) * m / (math.sqrt(l1 * (1 - l1 / n) ** 2) * math.sqrt(l2 * (1 - l2 / n) ** 2))


def pearsonIndex(s1, s2):
    pass
