from optparse import OptionParser
import numpy as np

import sys

sys.path.append("/home/utsav/Research/Hyrax/Utils/AndroidStats")
import AndroidStatsParser


def avglatency(latlist):
    return np.mean(latlist)


def avgCachehits(hitlist):
    return np.mean(hitlist)


def battery(batpath):
    f = open(batpath).readlines()
    f = [line.strip() for line in f]
    bat = AndroidStatsParser.getBatteryTrepn(f)
    return bat


def parse(result):
    res = open(result)
    lines = res.readlines()
    q = []
    r = []
    complat = []
    overalllat = []
    cachehits = []
    for line in lines:
        line = line.strip()
        chunks = line.split(",")
        q.append(chunks[0])
        r.append(chunks[1])
        complat.append(int(chunks[2]))
        overalllat.append(int(chunks[3]))
        if len(chunks) == 5:
            cachehits.append(int(chunks[4]))
        else:
            cachehits.append(0)
    return q, r, complat, overalllat, cachehits


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", type="str", dest="inpath", help="DB Input List")
    (options, args) = parser.parse_args()

    query, results, complatency, e2elat, cache = parse(options.inpath)
    print("Precision:{} Recall:{} CompLatency:{} E2ELat:{} Cache:{}".format(precision(query, results),
                                                                            recall(query, results),
                                                                            avglatency(complatency),
                                                                            avglatency(e2elat),
                                                                            avgCachehits(cache)))
