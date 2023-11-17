class BasicError(Exception):
	def __init__(self, message):
		super().__init__(message)
		self.message = message

	def __str__(self):
		return self.message

class EmptyTableError(BasicError):
	pass

class NoLinkFoundError(BasicError):
	pass

class NoMatchingLink(BasicError):
	pass