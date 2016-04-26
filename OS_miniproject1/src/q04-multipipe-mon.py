from mp1 import MP, MPthread
import random

# Q04:
# a. Complete the implementation of the MultiPurposePipe monitor below using
#    MPlocks and MPcondition variables. Your implementation should be able
#    to make progress if there are liquids that can flow
#
# b. What fairness properties does your implementation have?  Under what
#    conditions (if any) can a thread starve?
#
#    The fluid will be allowed to flow if the same kind of fluid is already flowing in the pipe.
#    The other type of fluids will be starving utill the fluids of same kind finished flowing.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class MultiPurposePipe(MP):
    """
    California has encountered another water crisis requiring new pipes to be
    built. The governor has decided to cut costs and introduce a new technology:
    multi-purpose pipes.  These pipes alternate carrying clean water and sewage.

    You are the lone civil engineer at the control station, and it is your job
    to make sure that people don't drink sewage. The multi-purpose pipe allows
    multiple instances of liquid to pass through in either direction but at any
    point in time, the liquid flowing through must be of the same type.

    Liquids wishing to flow should call the flow(), and once they have finished
    flowing, they should call finished()
    """

    def __init__(self):
        MP.__init__(self)
        # TODO
	#Lock for pipe control to make sure pipe control parameters race condition safe
	self.lckPipe    = self.Lock("LockPipe")
	#Condition variable for pipe control when to make a thread wait and and when to allow
	self.condPipe   = self.lckPipe.Condition("CondPipe")
	#Below variable helps to keep track of type of Liquid flowing the pipe currently.
	#Initialising it as 2 to indicate that nothing is flowing in the pipe.
	self.dir = 2
	#Below varible helps to keep track of number of multiple instance of 
	#same kind of fluids flowing in the pipe.
	self.count = 0
	
	self.lckCnt    = self.Lock("LockCount")
 
    def flow(self, direction):
        """wait for permission to flow through the pipe. direction should be
        either 0 or 1."""
        # TODO

	self.lckPipe.acquire()
	

	while (not self.dir == direction) and (not self.dir == 2):	
		self.condPipe.wait()
	
	self.dir = direction
		
	self.count += 1

	self.lckPipe.release()
    
    def finished(self,direction):
        # TODO
	self.lckPipe.acquire()
	
	self.count -= 1
	
	if self.count == 0:
		self.dir = 2
		self.condPipe.broadcast()

	self.lckPipe.release()	

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Sewage(MPthread):
    def __init__(self, pipe, id):
        MPthread.__init__(self, pipe, id)
        self.direction = 0
        self.wait_time = random.uniform(0.1,0.5)
        self.pipe      = pipe
        self.id        = id

    def run(self):
        # flush
        self.delay(self.wait_time)
        print "Sewage %d: trying to flow" % (self.id)
        # request permission to flow
        self.pipe.flow(self.direction)
        print "Sewage %d: Flowing" % self.id
        # flow through
        self.delay(0.01)
        print "Sewage %d: Flowed" % self.id
        # signal that we have finished flowing
        self.pipe.finished(self.direction)
        print "Sewage %d: Finished flowing" % self.id

class CleanWater(MPthread):
    def __init__(self, pipe, id):
        MPthread.__init__(self, pipe, id)
        self.direction = 1
        self.wait_time = random.uniform(0.1,0.5)
        self.pipe      = pipe
        self.id        = id

    def run(self):
        # turn on faucet
        self.delay(self.wait_time)
        print "CleanWater %d: Trying to flow" % (self.id)
        # request permission to flow
        self.pipe.flow(self.direction)
        print "CleanWater %d: Flowing" % self.id
        # flow through
        self.delay(0.01)
        print "CleanWater %d: Flowed" % self.id
        # signal that we have finished flowing
        self.pipe.finished(self.direction)
        print "CleanWater %d: Finished flowing" % self.id


if __name__ == "__main__":

    cityPipe = MultiPurposePipe()
    sid = 0
    cid = 0
    for i in range(100):
        if random.randint(0, 1) == 0:
            Sewage(cityPipe, sid).start()
            sid += 1
        else:
            CleanWater(cityPipe, cid).start()
            cid += 1


    cityPipe.Ready()
