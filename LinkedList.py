# Class to create a Linked List aka Inventory

class LinkedList:

	def __init__(self):
		self._head = None
		self._size = 0

	def __len__(self):
		return self._size

	def __contains__(self, target):
		curr_node = self._head
		while (curr_node is not None) and (curr_node.item != target):
			curr_node = curr_node.next
		return curr_node is not None

	def __getitem__(self, index):
		assert index < len(self), "Index can't be greater than the size of the bag!"
		curr_node = self._head
		i = 0
		while curr_node is not None:
			curr_node = curr_node.next
			i += 1

		if curr_node is None:
			return None
		else:
			return curr_node.item

	def index(self, target):
		curr_node = self._head
		index = 0
		while (curr_node is not None) and (curr_node.item != target):
			if curr_node.name == target:
				return index
			curr_node = curr_node.next
			index += 1
		return None

	def add(self, item, part_name):
		for i in self:
			if i.name == part_name:
				i.amount += 1
				return
		new_node = Node(item, part_name)
		item.amount += 1
		new_node.next = self._head
		self._head = new_node
		self._size += 1

	def remove(self, item, name=''):
		prev_node = None
		curr_node = self._head
		while (curr_node is not None) and (curr_node.item != item):
			prev_node = curr_node
			curr_node = curr_node.next

		assert curr_node is not None, "The item must be in the bag."
		if curr_node.name == name and item.amount >= 1:
			item.amount -= 1
		else:
			self._size -= 1
			if curr_node is self._head:
				self._head = curr_node.next
			else:
				prev_node.next = curr_node.next
			return curr_node.item

	def __iter__(self):
		return ListIterator(self._head)

	def __repr__(self):
		string = ''
		for i in self:
			string += '{} {}\n'.format(i.amount, i.name)
		return string


class Node(object):

	def __init__(self, item, name):
		self.item = item
		#self.amount = 0
		self.name = name
		self.next = None


class ListIterator:
	def __init__(self, listHead):
		self._curr_node = listHead

	def __iter__(self):
		return self

	def __next__(self):
		if self._curr_node is None:
			raise StopIteration
		else:
			item = self._curr_node.item
			self._curr_node = self._curr_node.next
			return item
