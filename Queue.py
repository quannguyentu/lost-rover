# Circular array
import ctypes


class Array:
	# Create an array with 'size' elements
	def __init__(self, size):
		assert size > 0, "Array size must be > 0"
		self._size = size
		# Create the array structure using the ctypes module
		PyArrayType = ctypes.py_object * size
		self._elements = PyArrayType()
		# Initialize each element
		self.clear(None)

	# Return the size of the array
	def __len__(self):
		return self._size

	# Get the content of the indexed element
	def __getitem__(self, index):
		assert 0 <= index < len(self), \
			"Array subscript out of range"
		return self._elements[index]

	# Set the value of the array element at the given index
	def __setitem__(self, index, value):
		assert 0 <= index < len(self), \
			"Array subscript out of range"
		self._elements[index] = value

	# Clear the array by setting each element to the given value
	def clear(self, value):
		for i in range(len(self)):
			self._elements[i] = value

	# Return the array's iterator for traversing the elements
	def __iter__(self):
		return _ArrayIterator(self._elements)


"""
An iterator for the Array ADT that allows the iteration of the array
object.
"""


class _ArrayIterator:

	def __init__(self, the_array):
		self._array_ref = the_array
		self._cur_ndx = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self._cur_ndx < len(self._array_ref):
			entry = self._array_ref[self._cur_ndx]
			self._cur_ndx += 1
			return entry
		else:
			raise StopIteration


class Queue:
	# Create a Circular Array with pointer and size
	def __init__(self, max_size=0):  # O(1)
		self._count = 0
		self._front = 0
		self._back = max_size - 1
		self._q_array = Array(max_size)

	# Check if the Queue is empty
	def is_empty(self):
		return self._count == 0

	# Check if the Queue is full
	def is_full(self):
		return self._count == len(self._q_array)

	def __len__(self):
		return self._count

	def peek(self):
		return self._q_array[self._front]

	# Add a item at the back
	def enqueue(self, item):
		# check if full
		if self.is_full():
			return
		max_size = len(self._q_array)
		# change the back pointer and add the item at the back
		self._back = (self._back + 1) % max_size
		self._q_array[self._back] = item
		# update the size
		self._count += 1

	# Delete a item at the front and return it
	def dequeue(self):
		# check if full
		assert not self.is_empty(), "..."
		# save the item
		item = self._q_array[self._front]
		max_size = len(self._q_array)
		# change the front pointer
		self._front = (self._front + 1) % max_size
		# update the size
		self._count -= 1
		# return the item
		return item
