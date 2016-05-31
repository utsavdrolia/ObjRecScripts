import os
from optparse import OptionParser
import shutil
from random import Random

parser = OptionParser()
parser.add_option("-i", "--input", type="str", dest="inpath", help="DB Input List")
parser.add_option("-d", "--output", type="str", dest="dbpath", help="New DB Directory")
parser.add_option("-q", "--qinput", type="str", dest="qinpath", help="Query Input List")
parser.add_option("-o", "--qoutput", type="str", dest="qdpath", help="New QB Directory")
parser.add_option("-n", "--num", type="int", dest="num", help="Number of query objects")

(options, args) = parser.parse_args()

# if os.path.exists(options.dbpath):
#     shutil.rmtree(options.dbpath)
# os.mkdir(options.dbpath)
#
# if os.path.exists(options.qdpath):
#     shutil.rmtree(options.qdpath)
# os.mkdir(options.qdpath)

num = options.num

outputfile = open("dblist.txt", "w")
lines = open(options.inpath).readlines()
for line in lines:
    line = line.strip()
    chunks = line.split("\t")
    imgname = chunks[1]
    imginpath = os.path.dirname(options.inpath) + os.sep + chunks[0]
    imgoutpath = "/home/objrec/ObjRecServer/db" + os.sep + imgname + ".jpg"
    # os.symlink(imginpath, imgoutpath)
    outputfile.write(imgname + "," + imgoutpath + "\n")

# objects = Random().sample(lines, num)
# qobjects = []
#
# for line in objects:
#     line = line.strip()
#     chunks = line.split("\t")
#     qobjects.append(chunks[1])
#
# outputfile = open(options.qdpath + os.sep + "querylist.txt", "w")
# lines = open(options.qinpath).readlines()
# Random().shuffle(lines)
# for line in lines:
#     line = line.strip()
#     chunks = line.split("\t")
#     imgname = chunks[1]
#     if imgname in qobjects:
#         imginpath = os.path.dirname(options.qinpath) + os.sep + chunks[0]
#         imgoutpath = options.qdpath + os.sep + os.path.basename(imginpath)
#         os.symlink(imginpath, imgoutpath)
#         outputfile.write(imgname + "," + imgoutpath + "\n")