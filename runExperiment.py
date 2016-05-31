import os
import sys
from optparse import OptionParser

import subprocess
from time import sleep

import CreateTrace

sys.path.append("/home/utsav/Research/Hyrax/Utils/AndroidUtils")
from AndroidUtils import AndroidUtils
from uploadImagesToDevice import upload_images

APP = "org.crowdcache.app"
CROWDACTIVITY = "MyActivity"
SERVERACTIVITY = "ServerActivity"
SERVER = "/usr/lib/jvm/java-7-oracle/bin/java -Djava.library.path=/home/utsav/OpenCV/opencv-2.4.12.3/build/lib -classpath /usr/lib/jvm/java-7-oracle/jre/lib/jfxrt.jar:/usr/lib/jvm/java-7-oracle/jre/lib/jce.jar:/usr/lib/jvm/java-7-oracle/jre/lib/javaws.jar:/usr/lib/jvm/java-7-oracle/jre/lib/charsets.jar:/usr/lib/jvm/java-7-oracle/jre/lib/jfr.jar:/usr/lib/jvm/java-7-oracle/jre/lib/plugin.jar:/usr/lib/jvm/java-7-oracle/jre/lib/resources.jar:/usr/lib/jvm/java-7-oracle/jre/lib/rt.jar:/usr/lib/jvm/java-7-oracle/jre/lib/deploy.jar:/usr/lib/jvm/java-7-oracle/jre/lib/management-agent.jar:/usr/lib/jvm/java-7-oracle/jre/lib/jsse.jar:/usr/lib/jvm/java-7-oracle/jre/lib/ext/sunec.jar:/usr/lib/jvm/java-7-oracle/jre/lib/ext/localedata.jar:/usr/lib/jvm/java-7-oracle/jre/lib/ext/sunjce_provider.jar:/usr/lib/jvm/java-7-oracle/jre/lib/ext/dnsns.jar:/usr/lib/jvm/java-7-oracle/jre/lib/ext/zipfs.jar:/usr/lib/jvm/java-7-oracle/jre/lib/ext/sunpkcs11.jar:/home/utsav/Research/CrowdCache/Code/ObjectRecognition/java/out/production/Server:/home/utsav/.m2/repository/org/zeromq/jeromq/0.3.4/jeromq-0.3.4.jar:/home/utsav/Research/CrowdCache/Code/ObjectRecognition/java/target/classes:/home/utsav/.m2/repository/org/boofcv/all/0.21/all-0.21.jar:/home/utsav/.m2/repository/org/boofcv/ip/0.21/ip-0.21.jar:/home/utsav/.m2/repository/org/boofcv/geo/0.21/geo-0.21.jar:/home/utsav/.m2/repository/org/boofcv/learning/0.21/learning-0.21.jar:/home/utsav/.m2/repository/org/boofcv/calibration/0.21/calibration-0.21.jar:/home/utsav/.m2/repository/org/boofcv/feature/0.21/feature-0.21.jar:/home/utsav/.m2/repository/org/boofcv/io/0.21/io-0.21.jar:/home/utsav/.m2/repository/com/thoughtworks/xstream/xstream/1.4.7/xstream-1.4.7.jar:/home/utsav/.m2/repository/xmlpull/xmlpull/1.1.3.1/xmlpull-1.1.3.1.jar:/home/utsav/.m2/repository/xpp3/xpp3_min/1.1.4c/xpp3_min-1.1.4c.jar:/home/utsav/.m2/repository/org/boofcv/recognition/0.21/recognition-0.21.jar:/home/utsav/.m2/repository/org/georegression/georegression/0.10/georegression-0.10.jar:/home/utsav/.m2/repository/org/ddogleg/ddogleg/0.9/ddogleg-0.9.jar:/home/utsav/.m2/repository/org/ejml/simple/0.29/simple-0.29.jar:/home/utsav/.m2/repository/org/ejml/dense64/0.29/dense64-0.29.jar:/home/utsav/.m2/repository/org/ejml/core/0.29/core-0.29.jar:/home/utsav/.m2/repository/org/ejml/equation/0.29/equation-0.29.jar:/home/utsav/.m2/repository/org/boofcv/sfm/0.21/sfm-0.21.jar:/home/utsav/.m2/repository/org/boofcv/visualize/0.21/visualize-0.21.jar:/home/utsav/OpenCV/opencv-2.4.12.3/build/bin/opencv-2412.jar:/home/utsav/Research/CrowdCache/Code/ObjectRecognition/java/out/production/Cache:/home/utsav/Research/CrowdCache/Code/ObjectRecognition/java/out/production/Hyrax:/home/utsav/Research/Hyrax/Hyrax/libs/jyre.jar:/home/utsav/Research/Hyrax/Hyrax/libs/guava-18.0.jar:/home/utsav/Research/Hyrax/Hyrax/libs/protobuf-java-3.0.0-alpha-4-pre.jar:/home/utsav/.m2/repository/org/apache/commons/commons-lang3/3.3.2/commons-lang3-3.3.2.jar:/home/utsav/Research/CrowdCache/Code/ObjectRecognition/java/out/production/Java-Naive-Bayes-Classifier org.crowdcache.server.ObjRecServer /home/utsav/Research/CrowdCache/DBImages/dblist.txt"
EXPERIMENT = "/home/utsav/Research/CrowdCache/Experiments/CloudletVM/"
MOBILELOG = "/sdcard/DCIM/Camera/Objects/log"
FINISHFILE="/sdcard/DCIM/Camera/Objects/finish"
OBJECTS = 50


def createuploadTrace(devs, endtime):
    objdir = CreateTrace.create_query_dir(
        "/home/utsav/Research/CrowdCache/UMissouri-Mobile/Database_images/_list_images.txt",
        "/home/utsav/Research/CrowdCache/UMissouri-Mobile/Query_images/_list_images.txt",
        OBJECTS)
    files = CreateTrace.create_trace(objdir,
                                     "/home/utsav/Research/CrowdCache/MobileQueryImages/",
                                     endtime,
                                     len(devs))
    for dev, tracef in zip(devs, files):
        upload_images(tracef, dev.strip())


def check_finish(devs):
    count = 0
    for dev in devs:
        AndroidUtils.get_file(FINISHFILE, os.curdir + "/finish", dev)
        if os.path.exists(os.curdir + "/finish"):
            count += 1
            os.remove(os.curdir + "/finish")
    if count == len(devs):
        return True
    return False


def launchProcess():
    return subprocess.Popen("exec " + SERVER, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def launchCrowd(devs, outdir):
    print("Launching Crowd")
    AndroidUtils.USBPowerOff()
    AndroidUtils.killAppOnAll(devs, APP)
    AndroidUtils.launchAppOnAll(devs, APP + "/." + CROWDACTIVITY)
    # server = launchProcess()
    AndroidUtils.trepn_start_profiling_all(devs)
    AndroidUtils.send_intent_to_all(devs, ["org.crowdcache.app.intent.EXPERIMENT", "--ei", "TIMEOUT", "1000"])

    sleep(30)
    while not check_finish(devs):
        print("Crowd running...")
        sleep(10)
    print("Finished Crowd")
    AndroidUtils.trepn_stop_profiling_all(devs)
    AndroidUtils.get_files(MOBILELOG, outdir + os.sep + "logs" + os.sep, devs)
    AndroidUtils.trepn_read_logs_all(devs, outdir + os.sep + "trepn" + os.sep)
    AndroidUtils.killAppOnAll(devs, APP)
    # server.kill()
    AndroidUtils.USBPowerOn()


def launchServer(devs, outdir):
    AndroidUtils.USBPowerOff()
    print("Launching Server")

    AndroidUtils.killAppOnAll(devs, APP)
    AndroidUtils.launchAppOnAll(devs, APP + "/." + SERVERACTIVITY)
    # server = launchProcess()
    AndroidUtils.trepn_start_profiling_all(devs)
    AndroidUtils.send_intent_to_all(devs, ["org.crowdcache.app.intent.EXPERIMENT"])

    sleep(30)
    while not check_finish(devs):
        print("Server running...")
        sleep(10)

    print("Finished Server")
    AndroidUtils.trepn_stop_profiling_all(devs)
    AndroidUtils.get_files(MOBILELOG, outdir + os.sep + "logs" + os.sep, devs)
    AndroidUtils.trepn_read_logs_all(devs, outdir + os.sep + "trepn" + os.sep)
    AndroidUtils.killAppOnAll(devs, APP)
    # server.kill()
    AndroidUtils.USBPowerOn()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--list", type="str", dest="devicelist", help="Device list")
    parser.add_option("-t", "--time", type="int", dest="endtime", help="End time")
    parser.add_option("-e", "--experiment", type="str", dest="experiment", help="Experiment name")
    (options, args) = parser.parse_args()

    devices = [d.strip() for d in open(options.devicelist).readlines()]
    # devices = ["192.168.1.3:5555"]

    AndroidUtils.kill_server()
    sleep(10)
    AndroidUtils.start_server()
    sleep(10)
    AndroidUtils.connect_all(devices)
    AndroidUtils.trepn_launch_all(devices)

    if options.experiment is None:
        for exp in range(4):
            t = 200*(2**exp)
            crowdout = EXPERIMENT + str(OBJECTS) + "_" + str(t) + os.sep + "Crowd"
            serverout = EXPERIMENT + str(OBJECTS) + "_" + str(t) + os.sep + "Server"
            print("Running Experiment for:{}".format(str(t)))
            for iteration in range(8):
                print("Running Iteration :{}".format(str(iteration)))
                crowdoutiter = crowdout + os.sep + str(iteration)
                serveroutiter = serverout + os.sep + str(iteration)
                if not os.path.exists(serveroutiter):
                    os.makedirs(serveroutiter)
                if not os.path.exists(crowdoutiter):
                    os.makedirs(crowdoutiter)
                createuploadTrace(devices, t)
                launchCrowd(devices, crowdoutiter)
                sleep(30)
                launchServer(devices, serveroutiter)
                # Recharge
                sleep(300)

    else:
        crowdout = EXPERIMENT + options.experiment + os.sep + "Crowd"
        serverout = EXPERIMENT + options.experiment + os.sep + "Server"
        if not os.path.exists(serverout):
            os.makedirs(serverout)
        if not os.path.exists(crowdout):
            os.makedirs(crowdout)
        # createuploadTrace(devices, options.endtime)
        launchServer(devices, serverout)
        sleep(30)
        launchCrowd(devices, crowdout)
