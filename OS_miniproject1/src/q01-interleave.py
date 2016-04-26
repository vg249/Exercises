from mp1 import MP, MPthread

# Q01:
# a. Run the following concurrent program. Are there any particular patterns in
#    the output? Is the interleaving of the output from the two threads
#    predictable in any way?
#
#    There is no any pattern in interleavig.
#    We cannot predict it any way.
#
# b. If the answer to part (a) is affirmative, run the same program while
#    browsing the web. Does the pattern you outlined in section (a) hold?
#
#   
#
# c. In general, can one rely on a particular timing/interleaving of executions
#    of concurrent processes?
#
#    No we cannot rely on particular timing/interleaving.
#    
#
# d. Given that there are no synchronization operations in the code below, any
#    interleaving of executions should be possible. When you run the code, do
#    you believe that you see a large fraction of the possible interleavings? If
#    so, what do you think makes this possible? If not, what does this imply
#    about the effectiveness of testing as a way to find synchronization errors?
#   
#    Yes there is a large fraction of possible interleavings
#    The random interleaving is depends on other process and threads running 
#    along with the threads. As we cannot be sure of switching between other processes
#    Any random interleaving is possible
#    

class Worker1(MPthread):
    def __init__(self, mp):
        MPthread.__init__(self, mp, "Worker 1")

    def run(self):
        while True:
            print("Hello from Worker 1")

class Worker2(MPthread):
    def __init__(self, mp):
        MPthread.__init__(self, mp, "Worker 2")

    def run(self):
        while True:
            print("Hello from Worker 2")
mp = MP()
w1 = Worker1(mp)
w2 = Worker2(mp)
w1.start()
w2.start()

##
## vim: ts=4 sw=4 et ai
##

