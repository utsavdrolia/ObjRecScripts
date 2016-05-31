import os
from optparse import OptionParser
from pprint import pprint

import time

import pickle

import cv2

import BruteForceMatcher

parser = OptionParser()
parser.add_option("-i", "--inputim", type="str", dest="inpath", help="Input Image")
parser.add_option("-d", "--db", type="str", dest="dbpath", help="DB of descriptors")

(options, args) = parser.parse_args()
BFM = BruteForceMatcher.BFM(options.dbpath)
# db = BruteForceMatcher.get_desc_dict(options.dbpath)
# DB = {}
# for im in db.keys():
#     kplist, deslist = db[im]
#     kp = []
#     for point in kplist:
#         temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
#                                     _octave=point[4], _class_id=point[5])
#         kp.append(temp_feature)
#     DB[im] = (kp, deslist)

lines = open(options.inpath).readlines()
queries = {}
for line in lines:
    line = line.strip()
    chunks = line.split("\t")
    img = os.path.dirname(options.inpath) + os.sep + chunks[0]
    gt = chunks[1]
    queries[img] = {"gt": gt, "result": None, "time": None}

for q in queries.keys():
    print("Matching:{}".format(q))
    cvimg = BruteForceMatcher.get_cvimg(q)
    start = time.time()
    res = BFM.match_input_all(cvimg)
    t = time.time() - start
    queries[q]["result"] = res
    queries[q]["time"] = t
    print("Res:{}".format(queries[q]))

pprint(queries)
pickle.dump(queries, open("results", "wb"))
