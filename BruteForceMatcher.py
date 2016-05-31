from optparse import OptionParser

import cv2
import pickle

import multiprocessing.dummy
import concurrent.futures as futures
import time

import numpy as np

from featureExtractor import extract_all


class BFM:
    def __init__(self, dbpath):
        self.DB = extract_all(dbpath)
        # self.pool = multiprocessing.dummy.Pool(processes=16)
        self.pool = futures.ThreadPoolExecutor(50)
        print("Initialized")

    def match_input_all(self, cvinputim):
        surf = cv2.SURF(400)
        imgkp, imgdes = surf.detectAndCompute(cvinputim, None)
        # imgkp = map(pickle_keypoints, imgkp)

        if imgdes is not None and len(imgdes) > 0:
            pairs = []
            for im in self.DB.keys():
                dbkp, dbdes = self.DB[im]
                pairs.append((dbdes, dbkp, imgdes, imgkp, im))
            results = self.pool.map(match_pair, pairs)
            return max(results, key=lambda x: x[1])
        return None


def pickle_keypoints(point):
    return point.pt, point.size, point.angle, point.response, point.octave, point.class_id


def unpickle_keypoints(point):
    return cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])


def get_desc_dict(dbpath):
    return pickle.load(open(dbpath, "rb"))


def get_cvimg(inpath):
    return cv2.imread(inpath, 0)


def match_pair(des):
    des1, kp1, des2, kp2, im = des
    # kp1 = map(unpickle_keypoints, kp1)
    # kp2 = map(unpickle_keypoints, kp2)
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    if len(good) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

    # print("Done:{} Match:{}".format(im, len(good)))
        return im, sum(matchesMask)

    return im, 0


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--inputim", type="str", dest="inpath", help="Input Image")
    parser.add_option("-d", "--db", type="str", dest="dbpath", help="DB of descriptors")

    (options, args) = parser.parse_args()

    DB = get_desc_dict(options.dbpath)
    cvimg = get_cvimg(options.inpath)
    start = time.time()
    print("Match Results:{}".format(match_input_all(cvimg, DB)))
    print("Time:{}".format(time.time() - start))
