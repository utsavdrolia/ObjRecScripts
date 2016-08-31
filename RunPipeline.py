import os
from optparse import OptionParser
import subprocess
from CreateDB import create
from FileSystemGlobals import *


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


def launch_pipeline(querypath, dbpath, resultpath, matchertype=str(2), featuretype=str(1)):
    subprocess.call([JAVA, JAVA_MAX_MEM, OPENCVLIB, CLASSPATH_STR, CLASSPATH, OR_PIPELINE, querypath, dbpath, resultpath, PARS[featuretype], PARS_DB[featuretype], matchertype, featuretype, MATCHER_PARS[matchertype]])


def run_pipeline(indbpath, outdbpath, num, inqpath, outqpath, descnum, resultspath, matchertype=str(2), featuretype=str(1)):
    '''
    Run the Object recognition server
    :param indbpath:
    :param outdbpath:
    :param num:
    :param inqpath:
    :param outqpath:
    :param descnum:
    :param resultspath:
    :param matchertype:
    :param featuretype:
    :return:
    '''
    dbfile, qfile = create(indbpath, outdbpath, num, inqpath, outqpath)
    change_num_desc(descnum, PARS[featuretype])
    launch_pipeline(qfile, dbfile, resultspath, matchertype, featuretype)


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
