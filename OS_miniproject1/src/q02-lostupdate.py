from mp1 import MP, MPthread

# Q02:
# This program simulates a postmodern game between two teams.  Each team
# presses their button as fast as they can.  There is a counter that starts at
# zero; the red team's increases a counter, while the blue team's button
# decreases the counter.  They each get to press their button 10000 times. If the
# counter ends up positive, the read team wins; a negative counter means the blue
# team wins.
#
# a. This game is boring: it should always end in a draw.  However, the provided
#    implementation is not properly synchronized.  When both threads terminate,
#    what are the largest and smallest possible scores?
#    
#    There is chance that for every instance of Red Team can override the Blue Team's score and viceverse.
#    That is because of race condition. And there is chance that it can happen every time.
#    So,The Largest Possible score is 10000
#    The smallest possible score is -10000
#
# b. What other values can the score have when both threads have terminated?
#   
#    In between 10000 and -10000, the score can be of any value as we cannot predict how the 
#    Interleavings will be
#
# c. Add appropriate synchronization such that updates to the counter
#    occur in a critical section, ensuring that the energy level is
#    always at 0 when the two threads terminate.
#
#    Your synchronization must still allow interleaving between the two threads.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class Contest(MP):
    def __init__(self):
        MP.__init__(self)
        self.counter = self.Shared("counter", 0)
        self.lock = self.Lock("LockForBoth")   #Lock is initialized for the process named Contest

    def pushRed(self):
        self.lock.acquire() #Red Team is acquring lock, to avoid any race condition casued by blue team
        self.counter.inc()
        self.lock.release() #thread releases the lock 


    def pushBlue(self):
        self.lock.acquire() #Blue Team is acquring lock, to avoid any race condition casued by red team
        self.counter.dec()
        self.lock.release() #The Tread releases the lock 

class RedTeam(MPthread):
    def __init__(self, contest):
        MPthread.__init__(self, contest, "Red Team")
        self.contest = contest     

    def run(self):
        for i in range(10000):
            self.contest.pushRed()

class BlueTeam(MPthread):
    def __init__(self, contest):
        MPthread.__init__(self, contest, "Blue Team")
        self.contest = contest

    def run(self):
        for i in range(10000):
            self.contest.pushBlue()

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

contest = Contest()
red  = RedTeam(contest)
blue = BlueTeam(contest)
red.start()
blue.start()
contest.Ready()

print("The counter is " + str(contest.counter.read()))

##
## vim: ts=4 sw=4 et ai
##
