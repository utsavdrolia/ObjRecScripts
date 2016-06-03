import os
from optparse import OptionParser
import shutil
from random import Random


'''
This script creates mini datasets and respective queries with noise from the original dataset
'''


NOISE = 0.1


def create_db(indbpath, outdbpath, num):
    indbitems = open(indbpath).readlines()
    Random().shuffle(indbitems)
    indbitems = [item.strip().split("\t") for item in indbitems]

    if num > len(indbitems):
        num = len(indbitems)

    qobjects = []
    nobjects = []

    # Create DB
    out = outdbpath + os.sep + "dblist.txt"
    outputfile = open(out, "w")
    for n in range(num):
        chunks = indbitems[n]
        imgname = chunks[1]
        qobjects.append(imgname)
        imginpath = os.path.dirname(indbpath) + os.sep + chunks[0]
        imgoutpath = outdbpath + os.sep + imgname + ".jpg"
        os.symlink(imginpath, imgoutpath)
        outputfile.write(imgname + "," + imgoutpath + "\n")

    # Create noise
    num_noise = int(num*NOISE)
    # make sure there are enough items in the DB to create noise
    if (len(qobjects) + num_noise) > len(indbitems):
        num_noise = len(indbitems) - len(qobjects)

    noisecounter = 0

    while noisecounter <= num_noise:
        item = Random().choice(indbitems)
        noisename = item[1]
        if noisename not in qobjects:
            nobjects.append(noisename)
            noisecounter += 1

    return out, qobjects, nobjects


def create_queries(qinpath, qdpath, qobjects, nobjects):
    # Create Queries
    lines = open(qinpath).readlines()
    out = qdpath + os.sep + "querylist.txt"
    outputfile = open(out, "w")
    Random().shuffle(lines)

    for line in lines:
        line = line.strip()
        chunks = line.split("\t")
        imgname = chunks[1]
        if imgname in qobjects:
            imginpath = os.path.dirname(qinpath) + os.sep + chunks[0]
            imgoutpath = qdpath + os.sep + os.path.basename(imginpath)
            os.symlink(imginpath, imgoutpath)
            outputfile.write(imgname + "," + imgoutpath + "\n")
        elif imgname in nobjects:
            imginpath = os.path.dirname(qinpath) + os.sep + chunks[0]
            imgoutpath = qdpath + os.sep + os.path.basename(imginpath)
            os.symlink(imginpath, imgoutpath)
            outputfile.write("Noise" + "," + imgoutpath + "\n")
    return out


def create(indbpath, outdbpath, num, qinpath, qdpath):

    if os.path.exists(outdbpath):
        shutil.rmtree(outdbpath)
    os.mkdir(outdbpath)

    if os.path.exists(qdpath):
        shutil.rmtree(qdpath)
    os.mkdir(qdpath)

    dbfile, q, n = create_db(indbpath, outdbpath, num)
    qfile = create_queries(qinpath, qdpath, q, n)
    return dbfile, qfile

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-i", "--input", type="str", dest="inpath", help="DB Input List")
    parser.add_option("-d", "--output", type="str", dest="dbpath", help="New DB Directory")
    parser.add_option("-q", "--qinput", type="str", dest="qinpath", help="Query Input List")
    parser.add_option("-o", "--qoutput", type="str", dest="qdpath", help="New QB Directory")
    parser.add_option("-n", "--num", type="int", dest="num", help="Number of objects")
    (options, args) = parser.parse_args()

    create(options.inpath, options.dbpath, options.num, options.qinpath, options.qdpath)
