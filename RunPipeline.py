import os
from optparse import OptionParser
import subprocess
from CreateDB import create

CLASSPATH = "/usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/java/opencv-2412.jar:/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/classes/artifacts/ObjectRecog/ObjectRecog.jar"
JAVA = "/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/bin/java"
OPENCVLIB = "-Djava.library.path=/usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/java"
CLASSPATH_STR = "-classpath"
OR_PIPELINE = "EvaluateOpenCV"
ORB_PARS = "/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/orb_pars.txt"
ORB_PARS_DB = "/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/orb_pars_db.txt"
JAVA_INIT_MEM = "-Xms1g"
JAVA_MAX_MEM = "-Xmx6g"
JAVA_GC = "-XX:+UseG1GC"



def change_num_desc(desc_num, pars_path):
    parsfile = open(pars_path)
    pars = parsfile.readlines()
    parsfile.close()

    for n in range(len(pars)):
        line = pars[n]
        if line.startswith("nFeatures"):
            pars[n] = "nFeatures: " + str(desc_num) + "\n"

    parsfile = open(pars_path, mode="w")
    parsfile.writelines(pars)
    parsfile.close()


def launch_pipeline(querypath, dbpath, resultpath, matchertype=str(1)):
    print(" ".join([JAVA, JAVA_MAX_MEM, OPENCVLIB, CLASSPATH_STR, CLASSPATH, OR_PIPELINE, querypath, dbpath, resultpath, ORB_PARS, ORB_PARS_DB, matchertype]))
    subprocess.call([JAVA, JAVA_MAX_MEM, OPENCVLIB, CLASSPATH_STR, CLASSPATH, OR_PIPELINE, querypath, dbpath, resultpath, ORB_PARS, ORB_PARS_DB, matchertype])


def run_pipeline(indbpath, outdbpath, num, inqpath, outqpath, descnum, parspath, resultspath, matchertype=str(1)):
    dbfile, qfile = create(indbpath, outdbpath, num, inqpath, outqpath)
    print ("DB:{}\nQ:{}".format(dbfile, qfile))
    change_num_desc(descnum, parspath)
    launch_pipeline(qfile, dbfile, resultspath, matchertype)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", type="str", dest="indbpath", help="DB Input List")
    parser.add_option("-d", "--output", type="str", dest="outdbpath", help="New DB Directory")
    parser.add_option("-q", "--qinput", type="str", dest="inqpath", help="Query Input List")
    parser.add_option("-o", "--qoutput", type="str", dest="outqpath", help="New QB Directory")
    parser.add_option("-n", "--num", type="int", dest="num", help="Number of objects in DB")
    parser.add_option("-s", "--descnum", type="int", dest="descnum", help="Number of Descriptors")
    parser.add_option("-p", "--parspath", type="str", dest="parspath", help="Path of pars file")
    parser.add_option("-r", "--resultpath", type="str", dest="resultpath", help="Path of result file")
    (options, args) = parser.parse_args()

    run_pipeline(os.path.abspath(options.indbpath),
                 os.path.abspath(options.outdbpath),
                 options.num,
                 os.path.abspath(options.inqpath),
                 os.path.abspath(options.outqpath),
                 options.descnum,
                 options.parspath,
                 os.path.abspath(options.resultpath))
