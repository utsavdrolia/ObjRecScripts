import json
import os
from optparse import OptionParser
import sys

sys.path.append("/Users/utsav/Documents/DATA/Research/HYRAX/Code/PlotterUtils")

from PlotterUtils import lineplot

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", type="str", dest="inpath", help="Path of Experiments")
    (options, args) = parser.parse_args()

    exp_dir = options.inpath
    recallarr = []
    precisionarr = []
    latarr = []
    ticks = {}
    legend = []
    o_dirs = [d for d in os.listdir(exp_dir) if d.startswith("O_")]
    o_dirs.sort(key=lambda x: int(x.split("_")[1]))

    for o_dir in o_dirs:
        if o_dir.startswith("O_"):
            o_name = o_dir
            o_number = o_name.split("_")[1]
            legend.append(o_number + " Objects")
            o_dir = exp_dir + os.sep + o_dir
            recall = []
            prec = []
            lat = []
            for desc_dir in os.listdir(o_dir):
                if desc_dir.startswith("D_"):
                    desc_name = desc_dir
                    desc_number = int(desc_name.split("_")[1])
                    ticks[desc_number] = 0
                    desc_dir = o_dir + os.sep + desc_dir
                    results = json.load(open(desc_dir + os.sep + "analysis"))
                    print("O:{} D:{} Analysis:{}".format(o_number, desc_number, results))
                    recall.append((desc_number, results["recall"]))
                    prec.append((desc_number, results["precision"]))
                    lat.append((desc_number, results["latency"]))

            recall.sort(key=lambda x: x[0])
            prec.sort(key=lambda x: x[0])
            lat.sort(key=lambda x: x[0])
            t, r = zip(*recall)
            recallarr.append(r)
            t, r = zip(*prec)
            precisionarr.append(r)
            t, r = zip(*lat)
            latarr.append(r)

    ticks = ticks.keys()
    ticks.sort()
    lineplot.lineplot_multi(recallarr, ticks, ylim=(0,1), legend=legend, xlabel="Number of Descriptors", ylabel="Recall",
                            title="RecallvsNumDescriptors", pdfflag=True, savepath=exp_dir)
    lineplot.lineplot_multi(precisionarr, ticks, ylim=(0,1), legend=legend, xlabel="Number of Descriptors", ylabel="Precision",
                            title="PrecisionvsNumDescriptors", pdfflag=True, savepath=exp_dir)
    lineplot.lineplot_multi(latarr, ticks, legend=legend, ylim=(0,1000), xlabel="Number of Descriptors", ylabel="Latency (ms)",
                            title="LatencyvsNumDescriptors", pdfflag=True, savepath=exp_dir)
