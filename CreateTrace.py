import os
from optparse import OptionParser
from pprint import pprint
from random import Random
from uploadImagesToDevice import upload_images


def create_query_dir(dinpath, qinpath, objects):
    lines = open(dinpath).readlines()
    objects = Random().sample(lines, objects)
    qobjects = {}
    # create list of objects
    for line in objects:
        line = line.strip()
        chunks = line.split("\t")
        qobjects[chunks[1]] = []
    lines = open(qinpath).readlines()
    Random().shuffle(lines)
    for line in lines:
        line = line.strip()
        chunks = line.split("\t")
        imgname = chunks[1]
        if imgname in qobjects:
            imginpath = os.path.dirname(qinpath) + os.sep + chunks[0]
            qobjects[imgname].append(imginpath)
    return qobjects


def create_timeline(objects, endtime):
    ret = Random().sample(xrange(endtime), objects)
    ret.sort()
    return ret


def create_trace(objects, outputdir, endtime, numdevs):
    tracefile = outputdir + os.sep + "trace"
    devrequestsmap = {}
    for obj in objects:
        queries = objects[obj]
        for dev in range(numdevs):
            if dev not in devrequestsmap:
                devrequestsmap[dev] = []
            devrequestsmap[dev].append(obj + "," + queries[dev % len(queries)])
    tracefiles = []
    for requestlist in devrequestsmap:
        trace = outputdir + os.sep + "trace" + str(requestlist)
        timeline = create_timeline(len(objects), endtime)
        Random().shuffle(devrequestsmap[requestlist])
        tracefile = open(trace, "w")
        count = 0
        for req in devrequestsmap[requestlist]:
            tracefile.write(req + "," + str(timeline[count]) + "\n")
            count += 1
        tracefiles.append(trace)

    return tracefiles


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-b", "--dinput", type="str", dest="dinpath", help="DB Input List")
    parser.add_option("-q", "--qinput", type="str", dest="qinpath", help="Query Input List")
    parser.add_option("-n", "--num", type="int", dest="numobjects", help="Number of query objects")
    parser.add_option("-d", "--devices", type="int", dest="devices", help="Number of devices")
    parser.add_option("-e", "--end", type="int", dest="endtime", help="Trace end time")
    parser.add_option("-o", "--qoutput", type="str", dest="outpath", help="Output Directory")
    parser.add_option("-l", "--list", type="str", dest="devicelist", help="Device list")
    (options, args) = parser.parse_args()

    if not os.path.exists(options.outpath):
        os.mkdir(options.outpath)

    objdir = create_query_dir(options.dinpath, options.qinpath, options.numobjects)
    files = create_trace(objdir, options.outpath, options.endtime, options.devices)
    devices = open(options.devicelist).readlines()
    for dev, tracef in zip(devices, files):
        upload_images(tracef, dev.strip())


