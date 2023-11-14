from unittest import TestCase, main
from parser import markup

class MarkUpTest(TestCase):
	'''
	Unit-тестирование функции mark_up файла parser.py
	'''
	def test_otchet_OS(self):
		self.assertEqual(
			mark_up('Microsoft Windows - Windows 10 version 21H1 ProfessionalWorkstation (x64)'),
			{
				'product' : 'Windows',
				'family' : '10',
            	'version' : '21H1',
            	'architect': 'x64'
			}
			)

	def test_otchet_PO(self):
		pass

	def test_api_OS(self):
		pass

	def test_api_PO(self):
		pass

if __name__ == '__main__':
	main()