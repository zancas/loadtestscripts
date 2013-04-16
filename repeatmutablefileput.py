#! /usr/bin/env python

import subprocess, time, os


print "shit"
def main():
    print "fuck"
    numrequests = 100#00
    width = str(len(str(numrequests)))
    prestring = "%."+width+"d start: %s\tstop: %s\tdelta: %.4s \n"
    HTTPCODE = '200'
    counter = 0
    HTTPNot200Count = 0
    trialtime = time.time()
    os.mkdir(str(trialtime))
    datafilename = '%s/mutabletestfilecontents'%trialtime 
    fh = open(datafilename,'w')
    fh.write('')
    fh.close()
    errorout = open('%s/errors.txt'%trialtime,'a')
    errorout.close()
    trialtimes = open('%s/trialtimes.txt'%trialtime,'a')
    trialtimes.close()
    putstring = '/home/arc/tahoe-lafs/bin/tahoe put %(localfile)s URI:SSK:%(capability)s' % \
        {'localfile':datafilename, 
         'capability':'vsrlppw5n5kftboj4vx4xsfnwi:6rqmx3e32nglkl3wnapiesv5czbiy63t7bokcczy4wjjhwhiwlnq'
         }
    putcommandlist = putstring.split()
    while counter < numrequests:
        fh = open('%s/mutabletestfilecontents'%trialtime,'w')
        counter = counter + 1
        writedata = str(counter%10)
        fh.write(writedata)
        fh.close()
        startt = time.time()
        print startt
        SubProcObj = subprocess.Popen(putcommandlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        SubProcObj.wait()
        stopt = time.time()
        deltat = stopt - startt
        deltatout = prestring % (counter, startt, stopt, deltat)
        trialtimes = open('%s/trialtimes.txt'%trialtime,'a')
        trialtimes.write(deltatout)
        trialtimes.close()
        SubProcComm = SubProcObj.communicate()
        HTTPCODE = SubProcComm[1].split()[0]
        if HTTPCODE != '200':
            errorout = open('%s/errors.txt'%trialtime,'a')
            HTTPNot200Count = HTTPNot200Count + 1
            thetime = time.time()
            errorstring = "At %s, on the %sth 'put' HTTPCODE is:  %s .\nComm Tuple is %s.\n" % (thetime, counter, HTTPCODE, SubProcComm)
            errorout = open('%s/errors.txt'%trialtime,'a')
            errorout.write(errorstring)
            errorout.close()
    
    trialstop = time.time()
    totaltime = (trialstop - trialtime)/3600.
    errorfrequencystr = str((HTTPNot200Count*1.0) / (counter*1.0))
    errorcountstring = "The number of responses to the put request, not headed by HTTP 200 Codes in %s attempts is: %s\n" % (counter, HTTPNot200Count) 
    errorout = open('%s/errors.txt'%trialtime,'a')
    errorout.write(errorcountstring)
    errorout.close()
    trialtimes.close()
    print "The %s request trial took a total of %.5s hours." % (numrequests, totaltime)

if __name__ == '__main__':
    main()
