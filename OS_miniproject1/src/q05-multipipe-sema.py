from mp1 import MP, MPthread
import random

# Q05:
# a. Complete the implementation of the MultiPurposePipe monitor below using
#    MPsema. Your implementation should be able to make progress if there are 
#    liquids that can flow
#  
# b. What fairness properties does your implementation have?  Under what
#    conditions (if any) can a thread starve?
#    
#    The implementation makes the opposite kind of liquid to wait untill
#    all of its kind of liquids stopped flowing.
#    Allows immediately if the liquid of same kind is waiting.

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
	#Semaphore for Pipe Controller. Only one instance of any fluid can use the critical sections of the controller at time.
	self.semaPipe  = self.Semaphore("PipeSema",1)		
	# Below variable is used as a flag to indicate the type of fluid flowing in the pipe.
	# When the "dir" is set to 2, it indicates that no liquid is flowing in the pipe.
	self.dir = 2;
	#Below count is used to check the number of instances of same kind of fluids flowing in the pipe.

	self.SewWaitCount = 0;  
	self.SewFlowCount = 0;  
	self.semaSewPipe   = self.Semaphore("SewPipeSema",0)

	self.CleanWaitCount = 0;  
	self.CleanFlowCount = 0;  
	self.semaCleanPipe = self.Semaphore("CleanPipeSema",0)

    def flow(self, direction):
        """wait for permission to flow through the pipe. direction should be
        either 0 or 1."""
        # TODO
	#
	self.semaPipe.procure()
	if direction == 0:
		if (self.CleanFlowCount > 0 or self.SewWaitCount > 0):
			self.SewWaitCount += 1
			self.semaPipe.vacate()
			self.semaSewPipe.procure()	
		else:
			self.SewFlowCount += 1
			self.semaPipe.vacate()
	else:
		if (self.SewFlowCount > 0 or self.CleanWaitCount > 0):
			self.CleanWaitCount += 1
			self.semaPipe.vacate()
			self.semaCleanPipe.procure()	
		else:
			self.CleanFlowCount += 1
			self.semaPipe.vacate()
		

    def finished(self,direction):
        # TODO
	self.semaPipe.procure()
	if (direction == 0):
		self.SewFlowCount -= 1
		if self.SewFlowCount == 0 and self.CleanWaitCount > 0:
			for i in range(0,self.CleanWaitCount):
				self.semaCleanPipe.vacate()
				self.CleanFlowCount = self.CleanWaitCount
				self.CleanWaitCount = 0
	else:
		self.CleanFlowCount -= 1
		if self.CleanFlowCount == 0 and self.SewWaitCount > 0:
			for i in range(0,self.SewWaitCount):
				self.semaSewPipe.vacate()
				self.SewFlowCount = self.SewWaitCount
				self.SewWaitCount = 0

	self.semaPipe.vacate()
		
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
