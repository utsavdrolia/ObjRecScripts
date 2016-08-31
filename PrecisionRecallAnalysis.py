from optparse import OptionParser
import numpy as np

NOISE = "Noise"
NONE = "None"


def precision(querylist, resultlist):
    global NONE
    precis = []
    for q, r in zip(querylist, resultlist):
        if r != NONE:
            if r == q:
                precis.append(1)
            else:
                precis.append(0)
    return np.mean(precis)


def recall(querylist, resultlist):
    global NONE
    rec = []
    for q, r in zip(querylist, resultlist):
        if q != NOISE:
            if r == q:
                rec.append(1)
            else:
                rec.append(0)
    return np.mean(rec)