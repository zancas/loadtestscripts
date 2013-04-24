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

trial_length = max(zeroshifted_trial_stoptimes)
x_margin = (trial_length/20)
alldelta_times = [float(tt[-1]) for tt in trialtime_lists]
longest_rtt_y = max(alldelta_times)
yaxis_height = longest_rtt_y+longest_rtt_y/3
print "The longest round trip took %s seconds." % longest_rtt_y
longest_trial_index = alldelta_times.index(longest_rtt_y)
longest_rtt_x = float(trialtime_lists[longest_trial_index][2])-trial_starttimes[0]
longest_point = (longest_rtt_x, longest_rtt_y)
annotation_offset = (0, longest_rtt_y/6)
longest_annotation_point = tuple( [sum(x) for x in zip(longest_point, annotation_offset)] )
longest_annotation = '(%.2f, %.2f)' % longest_point
plt.annotate(longest_annotation, longest_point, longest_annotation_point, 
             arrowprops={'linewidth':1, 'linestyle':'dashed'})
#plt.plot(longest_rtt_x, longest_rtt_y, 'gv', markersize=10) 
plt.plot(zeroshifted_trial_starttimes, alldelta_times, 'b.', markersize=2)
plt.plot(zeroshifted_trial_stoptimes, alldelta_times, 'b.', markersize=2)
plt.ylabel("Round Trip Times (seconds)")
plt.xlabel("Time From Beginning of the First Trial (seconds)")
plt.axis([-x_margin, trial_length+x_margin, 0, yaxis_height])
plt.title("Round Trip Times")
pngfilename = os.path.join(sys.argv[1], 'Round_Trip_Times.png')
plt.savefig(pngfilename)
print "The graphic is saved in %s." % (pngfilename,)
