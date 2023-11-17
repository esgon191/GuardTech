from unittest import TestCase, main
from clear import format_api, format_local

class ClearTest(TestCase):
	def test_format_local(self):
		self.assertEqual(
			format_local('Microsoft Windows - Windows 10 version 21H1 ProfessionalWorkstation (x64)'),
			'windows 10 21h1 x64'
		)

	def test_format_api(self):
		self.assertEqual(
			format_api('Windows 10 Version 21H1 for x64-based Systems'),
			'windows 10 21h1 x64-based'
		)

if __name__ == '__main__':
	main()