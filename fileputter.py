#! /usr/bin/env python

import subprocess, time, sys
from twisted.python.filepath import FilePath

def append_to_filepath(filepath, data, delimiter='\n'):
    if filepath.exists():
        prefixdata = filepath.getContent()
        data = delimiter.join( (prefixdata, data) )
    filepath.setContent(data)


def main():
    #Nicely format the output of the timing data.
    numrequests = int(sys.argv[1])
    width = str(len(str(numrequests)))
    prestring = "%."+width+"d start: %s\tstop: %s\tdelta: %.4s \n"

    #Start the timer at the last possible moment.
    trialtime = str(time.time())

    #Setup the directory/files where output will be stored.
    FilePath(trialtime).makedirs()
    testfilepath   = FilePath(trialtime).child('testfile')
    errorfilepath  = FilePath(trialtime).child('errors.txt')
    trialtimespath = FilePath(trialtime).child('trialtimes.txt')

    #Setup the command that will invoke tahoe via subprocess
    #Note: The script assumes it is being invoked by a tahoe-aware shell.
    if len(sys.argv) == 4 and sys.argv[2] == '--mutable':
        putstring = '/home/arc/tahoe-lafs/bin/tahoe put -u http://127.0.0.1:3456 %(localfile)s URI:SSK:%(capability)s' % \
        {'localfile': testfilepath.path,
         'capability':'%s' % sys.argv[3]
         }

    else:
        putstring = 'tahoe put -u http://127.0.0.1:3456 %s' % testfilepath.path
    putcommandlist = putstring.split()

    HTTPNot200Count = 0
    counter = 0
    while counter < numrequests:
        counter = counter + 1
        data_to_write = 'a'*55 + str(counter%10)
        append_to_filepath(testfilepath, data_to_write)
        startt = time.time()
        SubProcObj = subprocess.Popen(putcommandlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        SubProcObj.wait()
        stopt = time.time()
        deltat = stopt - startt
        deltatout = prestring % (counter, startt, stopt, deltat)
        append_to_filepath(trialtimespath, deltatout)
        SubProcComm = SubProcObj.communicate()
        HTTPCODE = SubProcComm[1].split()[0]
        if HTTPCODE != '200':
            HTTPNot200Count = HTTPNot200Count + 1
            thetime = time.time()
            errorstring = "At %s, on the %sth 'put' HTTPCODE is:  %s .\nComm Tuple is %s.\n" % \
                          (thetime, counter, HTTPCODE, SubProcComm)
            append_to_filepath(errorfilepath, errorstring)

    trialstop = time.time()
    totaltime = (trialstop - float(trialtime))/3600.
    errorcountstring = "The number of responses to the put request, not headed by HTTP 200 Codes in %s attempts is: %s\n" % (counter, HTTPNot200Count)
    append_to_filepath(errorfilepath, errorcountstring)
    print "The %s request trial took a total of %.5s hours." % (numrequests, totaltime)

if __name__ == '__main__':
    main()
