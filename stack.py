class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def peek(self):
		return self.items[len(self.items) - 1]

	def size(self):
		return len(self.items)

	def printstack(self):
		s = self
		while (not s.isEmpty()):
			print(s.pop())

	def toList(self, out):
		s = self
		while (not s.isEmpty()):
			out.append(s.pop())
		return out