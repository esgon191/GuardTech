from unittest import TestCase, main
from compare import markup
import sys
sys.path.insert(1, '../')
class MarkUpTest(TestCase):
	'''
	Unit-тестирование функции mark_up файла compare.py
	'''
	def test_basic(self):
		self.assertEqual(
				markup('windows 10 21h1 x64-based'),
				{
					'keywords' : ['10', '21h1', 'windows'],
        			'versions' : [],
        			'razr' : '64'
				}
			)
		self.assertEqual(
				markup('windows 7 32-bit'),
				{
					'keywords' : ['7', 'windows'],
        			'versions' : [],
        			'razr' : '32'
				}
			)
		self.assertEqual(
				markup('visual studio 2019 16.1'),
				{
					'keywords' : ['2019', 'studio', 'visual'],
        			'versions' : ['16.1'],
        			'razr' : None
				}
			)
		self.assertEqual(
				markup('powerpoint 2013 sp1'),
				{
					'keywords' : ['2013', 'powerpoint', 'sp1'],
        			'versions' : [],
        			'razr' : None
				}
			)
		self.assertEqual(
				markup('.net framework 3.5'),
				{
					'keywords' : ['.net', 'framework'],
        			'versions' : ['3.5'],
        			'razr' : None
				}
			)

	def test_includes(self):
		self.assertEqual(
			markup('visual studio 2019 16.6 includes 16.0 - 16.5'),
			{
				'keywords' : ['2019', 'studio', 'visual'],
        		'versions' : ['16.6', ('16.0', '16.5')],
        		'razr' : None
			}
			)

if __name__ == '__main__':
	main()