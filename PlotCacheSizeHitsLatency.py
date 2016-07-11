import json
import os
from optparse import OptionParser
import sys

sys.path.append("/Users/utsav/Documents/DATA/Research/HYRAX/Code/PlotterUtils")
sys.path.append("/Users/utsav/Documents/DATA/Research/HYRAX/Code/")

from PlotterUtils import dual_yaxis_lineplot
from PyCache.PerfectLFUCache import PerfectLFUCache
from PyCache.ZipfGenerator import ZipfGenerator
from PyCache.AggressiveLFUCache import AggressiveLFUCache

if __name__ == '__main__':
    lat = []
    ratios = []
    lfratios = []
    # Total dataset size
    N = 500
    print ("N:{}".format(N))

    cloudcomput_const = 1  # 400 images in 400ms
    network_latency = 70 # ms
    network_bw = 5.0/8 # MBps
    request_size = 50.0/1000 # MB per image
    nw_lat = network_latency + (request_size / network_bw) * 1000
    L = nw_lat + cloudcomput_const * N
    print ("L:{}".format(L))

    l = 2.0 # 2ms/object
    print ("l:{}".format(l))

    # Working set size
    w = int(0.75*N)
    # w = int(L/l)
    # w = 100
    print ("w:{}".format(w))

    # generate zipf
    z = ZipfGenerator(w, 0.5)

    # Number of queries = 100*w
    queries = [z.next() for n in range(10*w)]

    # Cache size as multiples of w
    # cache_sizes = [int((float(x)/40.0) * w) for x in range(0, 21)]
    cache_sizes = range(0, 200)

    for cache_size in cache_sizes:
        print ("Size:{}".format(cache_size))
        cache = PerfectLFUCache(cache_size)
        for q in queries:
            v = cache[q]
        print (len(cache))
        cache_lat = len(cache) * l
        # lfratio = cache.getleastratio()
        ratio = float(cache.getmisses())/len(queries)
        print ("Miss Ratio:{}".format(ratio))
        ratios.append((ratio, 0))
        lat.append((cache_lat + L * ratio, 0))
        # lfratios.append((lfratio, 0))

    diffratios = [ratios[0]]
    for r in range(1, len(ratios)):
        diffratios.append(((ratios[r][0] - ratios[r-1][0])/(cache_sizes[r] - cache_sizes[r-1]), 0))

    diffdiffratios = [diffratios[0]]
    for r in range(1, len(diffratios)):
        diffdiffratios.append(((diffratios[r][0] - diffratios[r - 1][0])/(cache_sizes[r] - cache_sizes[r-1]), 0))

    dual_yaxis_lineplot.dual_yaxis_plot(lat, ratios, cache_sizes, xlabel="Cache Size", y1label="Average Latency (ms)",
                                        y2label="Miss Ratio", title="CacheLatencyVsSize", legend=("Latency","Miss Ratio"),
                                        flag=False)
