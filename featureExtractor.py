from optparse import OptionParser
import os
import cv2
import pickle
import multiprocess
import time


def extract_feat(image):
    img1 = cv2.imread(image, 0)
    sift = cv2.SURF(1600)
    kp, des = sift.detectAndCompute(img1, None)
    return kp, des


def extract_fast(image):
    img1 = cv2.imread(image, 0)
    # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector()

    # find and draw the keypoints
    kp = fast.detect(img1, None)
    print "Threshold: ", fast.getInt('threshold')
    print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
    print "Total Keypoints with nonmaxSuppression: ", len(kp)


def extract_orb(image):
    img1 = cv2.imread(image, 0)
    # Initiate FAST object with default values
    fast = cv2.ORB()

    # find and draw the keypoints
    kp = fast.detect(img1, None)
    print "Total Keypoints: ", len(kp)


# each database image is stored in a directory of its own
def extract_and_return(imagedir):
    imname = os.path.basename(imagedir)
    image = None
    for im in os.listdir(imagedir):
        if im.endswith(".jpg"):
            image = imagedir + os.sep + im
            break
    kp, des = extract_feat(image)
    # kplist = []
    # for k in kp:
    #     temp = (k.pt, k.size, k.angle, k.response, k.octave, k.class_id)
    #     # To get encode back into cv2.KeyPoint
    #     # temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
    #     # temp_descriptor = point[6]
    #     kplist.append(temp)
    print("Image:{}\nNum. Feats.:{}".format(image, len(des)))
    return imname, kp, des


def extract_catogory(objectdir):
    imagedirs = [objectdir + os.sep + im for im in os.listdir(objectdir) if os.path.isdir(objectdir + os.sep + im)]
    # pool = multiprocess.Pool(processes=24)
    results = map(extract_and_return, imagedirs)
    db = {}
    for result in results:
        print(result[0])
        db[result[0]] = (result[1], result[2])
    return db


def extract_all(db):
    catdirs = [db + os.sep + im for im in os.listdir(db) if os.path.isdir(db + os.sep + im)]
    db = {}
    for cat in catdirs:
        db.update(extract_catogory(cat))

    return db

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-i", "--inputdir", type="str", dest="inpath", help="Dir of image folders")
    (options, args) = parser.parse_args()

    savepath = options.inpath + os.sep + "desc_db"
    start = time.time()
    extract_orb(options.inpath)
    print(time.time() - start)