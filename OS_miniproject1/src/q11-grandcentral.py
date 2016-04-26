from mp1 import MP, MPthread

# Q11:
# You are in charge of track assignemnts at Grand Central Station.
#
# The station has many tracks that a variety of trains use for loading and
# unloading passengers. For simplicity, we assume that all tracks can be used
# by any type of train: Amtrak, Metro-North, or Subway. Since both New Yorkers
# and politicians can be quite finicky, there are many regulations regarding
# how the tracks can be assigned to trains of each type. Additionally, since
# Grand Central Station is up and running almost 24/7, inpsectors must
# also be given access to the tracks. For simplicity, inspectors are
# treated as "trains" in the scheudling system.
#
# The rules are thus:
#
#   (a) There are no more than N tracks assigned to trains at any given time
#   (b) A Subway train may not begin to use a track if it would cause more than
#       80% of the tracks in use to be assigned to Subway trains
#   (c) Amtrak trains may not use a track if there are any Metro-North trains
#       currently at the station
#   (d) Likewise, Metro-North trains may not use a track if there are any Amtrak
#       trains currently at the station (The two lines compete for some of the
#       same customers, and refuse to share the station at any time, out of spite)
#   (e) Maintenance crews are always allowed priority access to the tracks
#       (subject to condition a).  No train should be allowed to use a track if
#       an inspector is waiting.
#
# The regulations make no guarantees about starvation.

# Implement the track assignement dispatcher monitor using MPlocks and
# MPcondition variables

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class Dispatcher(MP):
    def __init__(self, n):
        MP.__init__(self)
        self.MaxTracks     = n  # Max Tracks that can be allocated 
        self.cntTrains     = 0  # Count of number of trains that are in station
        self.lckStation    = self.Lock("StationLock")   # Dispacher lock. to avoid race condition
                                                        # of dispatcher shared variables
        self.lckIns        = self.Lock("InspectorLock") # Special lock for inspector as it cannot
                                                        # for other trains. If other train acquired lock, 
                                                        # it may need to wait untill others releases lock to indicate 
                                                        # its arrival to dispatcher
        # Condition to check regulations for train admittance.
        # Trains wait untill these regulations are satified
        self.condStation   = self.lckStation.Condition("Condition")
        self.cntSubway     = 0  # keep count of number of subway trains 
        self.cntAmtrak     = 0  # keep count of number of amtrak trains 
        self.cntMetroNorth = 0  # keep count of number of MetroNoth trains 
        self.insWaiting    = 0  # keep count of number of Inspector trains

    def subway_enter(self):
        self.lckStation.acquire()
        # Checks whether the regulation are satisfied, 
        # if the train was admitted to the stations. By adding one to existing train count the
        # conditions are cheked. Below condition also checks the Subway trains occuoying 80% of
        # available track and max tracs available
        while (self.cntTrains+1) > self.MaxTracks or (self.cntSubway+1) > (0.8*self.MaxTracks) \
              or self.insWaiting > 0:
            self.condStation.wait()
        self.cntTrains += 1 # if admitted the count of trains in station is increased
        self.cntSubway += 1 # Subway count is also increased
        self.lckStation.release()

    def subway_leave(self):
        self.lckStation.acquire()
        self.cntTrains -= 1     # When leaving the count for total trains and the respective 
        self.cntSubway-= 1      # train count is reduced by one
        self.condStation.broadcast() #Signals all the waiting trains.
        self.lckStation.release()
                

    def amtrak_enter(self):
        self.lckStation.acquire()
        # For amtrak, metroNorth condition is checked
        while (self.cntTrains+1) > self.MaxTracks or self.cntMetroNorth >= 1 \
              or self.insWaiting > 0:
            self.condStation.wait()
        self.cntTrains += 1
        self.cntAmtrak += 1
        self.lckStation.release()


    def amtrak_leave(self):
        self.lckStation.acquire()
        self.cntTrains -= 1
        self.cntAmtrak -= 1
        self.condStation.broadcast()
        self.lckStation.release()
        
    def metronorth_enter(self):
        self.lckStation.acquire()
        #for Metronorth Amtrak condition is checked
        while (self.cntTrains+1) > self.MaxTracks or self.cntAmtrak >= 1 \
              or self.insWaiting > 0:
            self.condStation.wait()
        self.cntTrains += 1
        self.cntMetroNorth += 1
        self.lckStation.release()

    def metronorth_leave(self):
        self.lckStation.acquire()
        self.cntTrains -= 1
        self.cntMetroNorth -= 1
        self.condStation.broadcast()
        self.lckStation.release()

    def inspector_enter(self):
        # Special lock for Inspectors 
        # as the common dispatched lock may be acquired by other trains
        self.lckIns.acquire()
        self.insWaiting += 1 # Inspector waiting count is added to condition of all other 
                             # trains so that they connot be admitted if insWaiting count is more
                             # than one.
        self.lckIns.release()

        self.lckStation.acquire()
        while (self.cntTrains+1) > self.MaxTracks:
            self.condStation.wait()
        self.cntTrains += 1
        self.lckStation.release()

    def inspector_leave(self):
        self.lckStation.acquire()

        self.cntTrains -= 1
        
        self.lckIns.acquire()
        self.insWaiting -= 1
        self.lckIns.release()
        
        self.condStation.broadcast()
        self.lckStation.release()

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

SUBWAY      = 0
AMTRACK     = 1
METRONORTH  = 2
INSPECTOR   = 3

class Train(MPthread):
    def __init__(self, train_type, dispatcher):
        MPthread.__init__(self, dispatcher, 'Train')
        self.train_type = train_type
        self.dispatcher = dispatcher

    def run(self):
        enters = [self.dispatcher.subway_enter,
                  self.dispatcher.amtrak_enter,
                  self.dispatcher.metronorth_enter,
                  self.dispatcher.inspector_enter]
        leaves = [self.dispatcher.subway_leave,
                  self.dispatcher.amtrak_leave,
                  self.dispatcher.metronorth_leave,
                  self.dispatcher.inspector_leave]
        names  = ['subway', 'amtrak', 'metro north', 'inspector']

        print("%s train trying to arrive" % names[self.train_type])
        enters[self.train_type]()
        print("%s train admitted" % names[self.train_type])
        self.delay(0.1)
        print("%s train leaving" % names[self.train_type])
        leaves[self.train_type]()
        print("%s train done" % names[self.train_type])

max_trains = 15
numbers = [10, 35, 2, 4]
dispatcher = Dispatcher(max_trains)
for t in [SUBWAY, AMTRACK, METRONORTH, INSPECTOR]:
    for i in range(numbers[t]):
        Train(t, dispatcher).start()

##
## vim: ts=4 sw=4 et ai
##
