import os
import sys
from optparse import OptionParser

sys.path.append("/home/utsav/Research/Hyrax/Utils/AndroidUtils")
from AndroidUtils import AndroidUtils

REMOTE = "/sdcard/DCIM/Camera/Objects/"
LISTOFIMAGES = "qlist.txt"


def upload_images(listfile, dev):
    AndroidUtils.mkdir(dev, REMOTE)
    remotelist = open(LISTOFIMAGES, "w")
    lines = open(listfile).readlines()
    for line in lines:
        line = line.strip()
        chunks = line.split(",")
        imgname = chunks[0]
        imginpath = chunks[1]
        t = chunks[2]
        imgoutpath = REMOTE + os.path.basename(imginpath)
        AndroidUtils.send_file(imginpath, imgoutpath, dev)
        remotelist.write(imgname + "," + imgoutpath + "," + t + "\n")
    remotelist.close()
    AndroidUtils.send_file(LISTOFIMAGES, REMOTE + LISTOFIMAGES, dev)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-q", "--qinput", type="str", dest="qinpath", help="Query Input List")
    parser.add_option("-d", "--devices", type="str", dest="devices", help="device")
    (options, args) = parser.parse_args()
    upload_images(options.qinpath, options.devices)

