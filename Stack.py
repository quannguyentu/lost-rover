"""Create Stack class for Portal class"""


class _StackNode:
	def __init__(self, item, link):
		self.item = item
		self.link = link


class Stack:
	def __init__(self):
		self._head = None
		self._size = 0

	def peek(self):
		if self._size == 0:
			return 'Stack empty'
		else:
			return self._head.item

	def push(self, item):
		# ''' Method to push an item to the top of a Stack
		# '''
		node = _StackNode(item, self._head)
		self._head = node
		self._size += 1

	def pop(self):
		# ''' Method to pop an item from the top of a Stack
		# '''
		if self._size == 0:
			print('Stack empty')
			return None
		else:
			top_node = self._head
			self._head = self._head.link
			self._size -= 1
			return top_node.item

	def __len__(self):
		# ''' Overrides the Python len() method for Stack objects
		# '''
		return self._size

	def is_empty(self):
		# ''' Used to tell us whether the Stack is empty (returns a True or False)
		# '''
		return self._size == 0
