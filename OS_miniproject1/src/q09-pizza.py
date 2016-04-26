from mp1 import MP, MPthread
import random

# Q09:
# This program simulates the creation of pepperoni pizzas.
#
# Implement the PepperoniPizza monitor below using MPlocks and
# MPcondition variables.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class PepperoniPizzaMonitor(MP):
    """
    A pepperoni pizza is made from one pepperoni and three cheeses (each
    pepperoni and cheese can be used in only one pizza).  A thread offers an
    ingredient by calling the appropriate method; the thread will block until
    the ingredient can be used in the pizza.
    """

    def __init__(self):
        MP.__init__(self)
        # TODO
	self.lckPepperoni   = self.Lock("LckPepperoni")	# Lock for peperonni
	self.condPepperoni  = self.lckPepperoni.Condition("CondPepperoni") # Condition for pepperoni on
									   # When to go to sleep
	self.lckCheese	    = self.Lock("LckCheese")	# Lock for Cheese
	self.condCheese     = self.lckCheese.Condition("CondCheese")	# Condition for Cheese on 
									# when to go to sleep
	self.countPepWait   = 0	# Count for number of Peperoni's waiting
	self.countCheWait   = 0 # Count for number of Cheeses Waiting
	self.pepSendBake    = 0 # Count for number of peperoni matched with 3 cheeses
	self.cheSendBake    = 0 # Count for number of Chesses matched with one peperoni


    def pepperoni_ready(self):
        """Offer a pepperoni and block until this pepperoni can be used to make
        a pizza."""
        # TODO
	self.lckPepperoni.acquire()
	
	self.countPepWait += 1 # Peperoni ready, waiting
	
	# Checks the problem condition, 3 cheese and one peperonni for one pizza
	if self.countCheWait >=  3 and self.countPepWait >= 1:
	# Once condition satisfied matching is done
		self.pepSendBake += 1	# Increment Matched peperoni count by 1	
		self.countPepWait -= 1	# Waiting Peperoni count is reduced by 1	                            
		self.condPepperoni.signal() # wake up sleeping peperonis as pizza requirement is complete
		self.lckCheese.acquire()   
		self.cheSendBake += 3   # Increment Matched Cheese count by 3
		self.countCheWait -= 3	# Waiting Cheese count is reduced by 3, as 3 is the matching condition
		self.condCheese.broadcast() # wake up sleeping cheese as pizza requirement is complete  
		self.lckCheese.release()	
	
	# Wait if there is no peperoni matched with 3 cheses
	while self.pepSendBake < 1:
		self.condPepperoni.wait()
	
	self.pepSendBake -= 1 # Reduce the match count when sending to bake
	
	self.lckPepperoni.release()	

    def cheese_ready(self):
        """Offer a cheese and block until this cheese can be used to make a
        pizza."""
        # TODO
	self.lckCheese.acquire()
	
	self.countCheWait += 1 # Cheese ready, Increment waiting count
	
	# Checks the problem condition, 3 cheese and one peperonni for one pizza
	if self.countCheWait >=  3 and self.countPepWait >= 1:
	# Once condition satisfied matching is done
		self.cheSendBake += 3   # Increment Matched Cheese count by 3
		self.countCheWait -= 3	# Waiting Cheese count is reduced by 3, as 3 is the matching condition
		self.lckPepperoni.acquire()
		self.countPepWait -= 1	# Waiting Peperoni count is reduced by 1	                            
		self.pepSendBake += 1	# Increment Matched peperoni count by 1	
		self.condPepperoni.signal() # wake up sleeping peperonis as pizza requirement is complete 
		self.lckPepperoni.release() 
		self.condCheese.broadcast() # wake up sleeping cheeses as pizza requirement is complete	 
	
	# Wait if 3 cheeses are not matched with one peperoni
	while self.cheSendBake < 1:
		self.condCheese.wait()
	
	self.cheSendBake -= 1 # Reduce Cheese count when sending to bake
	
	self.lckCheese.release()	
	
	

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Pepperoni(MPthread):
    def __init__(self, pizza, id):
        MPthread.__init__(self, pizza, id)
        self.pizza = pizza
        self.id = id

    def run(self):
        while True:
            print "Pepperoni %d ready" % self.id
            self.pizza.pepperoni_ready()
            print "Pepperoni %d is in the oven" % self.id
            self.delay()
            print "Pepperoni %d finished baking" % self.id

class Cheese(MPthread):
    def __init__(self, pizza, id):
        MPthread.__init__(self, pizza, id)
        self.pizza = pizza
        self.id = id

    def run(self):
        while True:
            print "Cheese %d ready" % self.id
            self.pizza.cheese_ready()
            print "Cheese %d is in the oven" % self.id
            self.delay(0.5)
            print "Cheese %d finished baking" % self.id

if __name__ == '__main__':
    NUM_PEPPERONI = 5
    NUM_CHEESE = 6

    pizza = PepperoniPizzaMonitor()

    for i in range(NUM_PEPPERONI):
        Pepperoni(pizza, i).start()

    for j in range(NUM_CHEESE):
        Cheese(pizza, j).start()

    pizza.Ready()
