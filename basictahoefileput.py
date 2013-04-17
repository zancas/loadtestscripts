#! /usr/bin/env python

import subprocess, time
from twisted.python.filepath import FilePath

def append_to_filepath(filepath, data, delimiter='\n'):
    prefixdata = filepath.getContent()
    if prefixdata != '':
        data = delimiter.join( (prefixdata, data) )
    filepath.setContent(data)
    

def main():
    numrequests = 10000
    width = str(len(str(numrequests)))
    prestring = "%."+width+"d start: %s\tstop: %s\tdelta: %.4s \n"
    counter = 0
    HTTPNot200Count = 0
    trialtime = str(time.time())
    testfilepath   = FilePath(trialtime).child('testfile')
    errorfilepath  = FilePath(trialtime).child('errors.txt')
    trialtimespath = FilePath(trialtime).child('trialtimes.txt')
    # The script assumes it is being invoked by a tahoe-aware shell.
    putstring = 'tahoe put %s' % testfilepath.path
    putcommandlist = putstring.split()
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
    totaltime = (trialstop - trialtime)/3600.
    errorfrequencystr = str((HTTPNot200Count*1.0) / (counter*1.0))
    errorcountstring = "The number of responses to the put request, not headed by HTTP 200 Codes in %s attempts is: %s\n" % (counter, HTTPNot200Count) 
    append_to_filepath(errorfilepath, errorcountstring)
    print "The %s request trial took a total of %.5s hours." % (numrequests, totaltime)

if __name__ == '__main__':
    main()
