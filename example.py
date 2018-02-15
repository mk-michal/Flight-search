

class A:
	def __init__(self, chat):
		self.chat = chat
		print('first')

	def method1(self):
		self.state = 'SEND'
		print(self.state)

	def printer(self):
		print (self.state)


class B(A):
	def __init__(self, mandarin = 5):
		self.mandarin = mandarin
		print('second')
		print(self.mandarin)

	def method2(self):
		self.method1()
		print (self.state)