from unittest import TestCase, main
from compare import compare

class CompareTest(TestCase):
	def test_basic(self):
		self.assertEqual(
			compare(
				'Windows 10 Version 21H1 for x64-based Systems',
				'Microsoft Windows - Windows 10 version 21H1 ProfessionalWorkstation (x64)'	
			),
			[2, 2, 2]
		)
		self.assertEqual(
			compare(
				'Microsoft Windows Server 2003 x64 Edition Service Pack 2',
				'Microsoft Windows - Windows 10 version 21H1 ProfessionalWorkstation (x64)'	
			),
			[0, 2, 2]
		)

	def test_multi_versions(self):
		self.assertEqual(
			compare(
				'Microsoft .NET Framework 3.5 AND 4.6/4.6.1/4.6.2',
				'Microsoft .NET Framework - 3.5'
			),
			[2, 2, 1]
		)

if __name__ == '__main__':
	main()