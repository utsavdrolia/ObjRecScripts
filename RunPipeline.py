import os
from optparse import OptionParser
import subprocess
from CreateDB import create

CLASSPATH = "/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/javafx-doclet.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/lib/tools.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/htmlconverter.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/target/test-classes:/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/target/classes:/Users/utsav/.m2/repository/org/boofcv/all/0.21/all-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/ip/0.21/ip-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/geo/0.21/geo-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/learning/0.21/learning-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/calibration/0.21/calibration-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/feature/0.21/feature-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/io/0.21/io-0.21.jar:/Users/utsav/.m2/repository/com/thoughtworks/xstream/xstream/1.4.7/xstream-1.4.7.jar:/Users/utsav/.m2/repository/xmlpull/xmlpull/1.1.3.1/xmlpull-1.1.3.1.jar:/Users/utsav/.m2/repository/xpp3/xpp3_min/1.1.4c/xpp3_min-1.1.4c.jar:/Users/utsav/.m2/repository/org/boofcv/recognition/0.21/recognition-0.21.jar:/Users/utsav/.m2/repository/org/georegression/georegression/0.10/georegression-0.10.jar:/Users/utsav/.m2/repository/org/ddogleg/ddogleg/0.9/ddogleg-0.9.jar:/Users/utsav/.m2/repository/org/ejml/simple/0.29/simple-0.29.jar:/Users/utsav/.m2/repository/org/ejml/dense64/0.29/dense64-0.29.jar:/Users/utsav/.m2/repository/org/ejml/core/0.29/core-0.29.jar:/Users/utsav/.m2/repository/org/ejml/equation/0.29/equation-0.29.jar:/Users/utsav/.m2/repository/org/boofcv/sfm/0.21/sfm-0.21.jar:/Users/utsav/.m2/repository/org/boofcv/visualize/0.21/visualize-0.21.jar:/Users/utsav/Documents/DATA/Research/HYRAX/Code/JavaOR/classes/production/Cache:/usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/java/opencv-2412.jar"
JAVA = "/Library/Java/JavaVirtualMachines/jdk1.7.0_51.jdk/Contents/Home/bin/java"
OPENCVLIB = "-Djava.library.path=/usr/local/Cellar/opencv/2.4.12_2/share/OpenCV/java"
CLASSPATH_STR = "-classpath"
OR_PIPELINE = "EvaluateOpenCV"


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


def launch_pipeline(querypath, dbpath, resultpath):
    subprocess.call([JAVA, OPENCVLIB, CLASSPATH_STR, CLASSPATH, OR_PIPELINE, querypath, dbpath, resultpath])


def run_pipeline(indbpath, outdbpath, num, inqpath, outqpath, descnum, parspath, resultspath):
    dbfile, qfile = create(indbpath, outdbpath, num, inqpath, outqpath)
    print ("DB:{}\nQ:{}".format(dbfile, qfile))
    change_num_desc(descnum, parspath)
    launch_pipeline(qfile, dbfile, resultspath)


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
