The MP1 library provides thin wrappers around the python semaphore and monitor
classes.  It provides some helpful debug output, and makes grading submissions
easier.  You are required to use this library for MP1.

Using the MP1 library
---------------------

To use the library, import the MP and MPthread modules.

	from mp1 import MP, MPthread

Monitors and other classes to be used for sharing data between
threads should extend the MP class:

	class MPExample(MP):
		def __init__(self):
			MP.__init__(self, None)
			...

You may find it helpful to turn debugging on.  You can do this by setting the
`debug` variable to true:

		def __init__(self):
			MP.__init__(self, None)
			self.debug = True
			...

To create shared mutable variables, use the Shared method of the MP class:

	class MPExample(MP):
		def __init__(self):
			MP.__init__(self, None)
			self.myVariable = self.shared("myVariable", INITIAL_VALUE)

Shared variables should be updated by using the `read` and `write` methods:

		def increment(self):
			self.myVariable.write(self.myVariable.read() + 1)


Variable that are not shared between threads (e.g. local variables) can just be
declared and used as usual.

Creating a monitor with MP1 
---------------------------

See [the attached code](mp1-monitor-example.py)

Python does not have built-in support for monitors.  Instead, monitor code must
explicitly create a monitor lock, and create condition variables that refer to
that lock:

	class MonitorExample(MP):
		def __init__(self):
			MP.__init__(self, None)
			self.value = self.Shared("value", 0)
			self.lock  = self.Lock("monitor lock")
			self.gt0   = self.lock.Condition("value greater than 0")
			self.lt2   = self.lock.Condition("value less than 2")


Monitor methods should all acquire the monitor lock using the `with`
construct.  For example, using the MP1 library:

		def get_value(self):
			with self.lock:
				return self.value.read()

To block on a condition variable, call `wait`:

		def block_until_pos(self):
			with self.lock:
				while not (self.value.read() > 0):
					self.gt0.wait()

To notify a single blocked thread, call `signal`.  To notify all blocked
threads, call `broadcast`.  In other libraries, `signal` and `broadcast` are
sometimes called `notify` and `notifyAll`:

		def update(self, value):
			with self.lock:
				self.value.write(value)
				if self.value.read() > 0:
					self.gt0.signal()
				if self.value.read() < 2:
					self.lt2.broadcast()

Using semaphores with MP1
-------------------------

See [the attached code](mp1-semaphore-example.py).

To create a semaphore, use the `Semaphore` method of the `MP` class:

	class SemaphoreExample(MP):
		def __init__(self):
			MP.__init__(self, None)
			self.value     = self.Shared("value", 0)
			self.valueLock = self.Semaphore("value lock", 1)

The `P` and `V` methods are called `procure` and `vacate`:

		def update(self, newValue):
			self.valueLock.procure()
			self.value = newValue
			self.valueLock.release()

Creating threads with MP1
-------------------------

Classes representing threads should extend the MPthread class. the constructor
to MPthread takes an MP instance and a name:

	class ExampleThread(MPthread):
		def __init__(self, mp, name):
			MPthread.__init__(self, mp, name)
			...

Threads should implement the `go` function (**not `run`**):

		def go(self):
			print "starting"
			print "doing stuff"
			print "done"

This function will be called when the thread begins execution.


To cause the thread to begin, you should call `start`:

	ExampleThread(mp, "t1").start()

When the threads have been created, call:

	mp.Ready()

This will make all of the threads runnable, and will block until all of them
have completed (i.e. have finished running their `go` methods).


Threads can sleep for a while using delay():

		def go(self):
			...
			self.delay(2)		# sleep for at least 2 seconds
			...

