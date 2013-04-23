#! /usr/bin/env python

import sys, os
import matplotlib.pyplot as plt
import matplotlib.axis as axis
from twisted.python.filepath import FilePath

trialtimes_filepath = FilePath(sys.argv[1]).child('trialtimes.txt')
trialtime_lists = [x.split() for x in trialtimes_filepath.getContent().splitlines()]

trial_starttimes = [float(tt[2]) for tt in trialtime_lists]
zeroshifted_trial_starttimes = [ x - trial_starttimes[0] for x in trial_starttimes]
trial_stoptimes = [float(tt[4]) for tt in trialtime_lists]
zeroshifted_trial_stoptimes = [ x - trial_starttimes[0] for x in trial_stoptimes]

alldelta_times = [float(tt[-1]) for tt in trialtime_lists]
longest_rtt = max(alldelta_times)
print "longest_rtt is %s" % longest_rtt
longest_rtt_afterstart = float(trialtime_lists[alldelta_times.index(longest_rtt)][2])-trial_starttimes[0]
plt.plot(longest_rtt_afterstart, longest_rtt, 'gv', markersize=10) 
plt.plot(zeroshifted_trial_starttimes, alldelta_times, 'b.', markersize=2)
plt.plot(zeroshifted_trial_stoptimes, alldelta_times, 'b.', markersize=2)
plt.ylabel("Round Trip Times (s)")
plt.xlabel("Time From Beginning of the First Trial (s)")
plt.axis([-150, max(zeroshifted_trial_stoptimes)+150, 0, 7.25])
plt.title("Round Trip Times")
pngfilename = os.path.join(sys.argv[1], 'Round_Trip_Times.png')
plt.savefig(pngfilename)
print "The graphic is saved in %s." % (pngfilename,)
