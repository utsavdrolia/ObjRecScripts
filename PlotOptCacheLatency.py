from collections import Counter
import sys
import random

import numpy as np

sys.path.append("/Users/utsav/Documents/DATA/Research/HYRAX/Code/PlotterUtils")
sys.path.append("/Users/utsav/Documents/DATA/Research/HYRAX/Code/")

from PlotterUtils import dual_yaxis_lineplot
from PyCache.OptCache import OptCache
from PyCache.ZipfGenerator import randZipf
from PlotterUtils import lineplot

if __name__ == '__main__':


    # Total dataset size
    N = 2000
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
    w = int(1.0*N)
    # w = int(L/l)
    # w = 100
    print ("w:{}".format(w))

    # Interval for optimization
    # interval = 0.2*w
    # interval = 0.8*N
    # interval = 1

    # generate zipf
    # z = ZipfGenerator(w, 0.5)


    # Number of queries = 100*w

    # queries = [random.normalvariate(0, w - 1) for n in range(100000)]

    # Cache size as multiples of w
    # cache_sizes = [int((float(x)/40.0) * w) for x in range(0, 21)]
    priors = None
    cache = OptCache(N)
    for i in [1, 2]:
        queries = randZipf(w, i*0.4, 10000)
        lat = []
        ratios = []
        cache_sizes = []

        qcounter = 0
        counter = Counter(queries)
        for q in queries:
            qcounter += 1
            counter[q] += 1
            pre_miss = cache.getmisses()
            v = cache[q]
            cache_lat = len(cache) * l
            post_miss = cache.getmisses()
            lat.append(cache_lat + L * (post_miss - pre_miss))
            cache_sizes.append(len(cache))
            ratio = float(cache.getmisses()) / qcounter
            ratios.append(ratio)
        priors = cache.getcounter()
        # lfratio = cache.getleastratio()

        # print ("Miss Ratio:{}".format(ratios[-1]))
        print ("Latency:{}".format(sum(lat)/qcounter))
        print ("L:{}".format(L))

        lat = list(np.convolve(lat, np.ones((N,)) / N, mode='valid').tolist())
        len_lat = len(lat)
        for pad in range(len(queries) - len_lat):
            lat.insert(0, lat[0])

        dual_yaxis_lineplot.dual_yaxis_plot(ratios, cache_sizes, range(len(queries)), xlabel="Query Number",
                                            y1label="Miss Ratio",
                                            y1lim = (0, 1),
                                            y2label="Cache size", title="LatencySizeVsTime",
                                            legend=("Miss Ratio", "Cache size"),
                                            flag=False)

        dual_yaxis_lineplot.dual_yaxis_plot(lat, cache_sizes, range(len(queries)), xlabel="Query Number",
                                            y1label="Latency",
                                            y2label="Cache size", title="RatioSizeVsTime",
                                            legend=("Latency", "Cache size"),
                                            flag=False)

    # print(len(lat))
    # lineplot.lineplot_multi([counter.values()], counter.keys(), xlabel="Query Number", ylabel="Latency (ms)",
    #                         title="LatencyVsTime", flag=False)
