from unittest import TestCase, main
from compare import markup

class MarkUpTest(TestCase):
	'''
	Unit-тестирование функции mark_up файла compare.py
	'''
	def test_basic(self):
		self.assertEqual(
				markup('windows 10 21h1 x64'),
				{
					'keywords' : ['windows', '10', '21h1'],
        			'version' : None,
        			'razr' : '64'
				}
			)
		self.assertEqual(
				markup('windows 7 32-bit'),
				{
					'keywords' : ['windows', '7'],
        			'version' : None,
        			'razr' : '32'
				}
			)
		self.assertEqual(
				markup('visual studio 2019 16.1'),
				{
					'keywords' : ['visual', 'studio', '2019'],
        			'version' : '16.1',
        			'razr' : None
				}
			)
		self.assertEqual(
				markup('powerpoint 2013 sp1'),
				{
					'keywords' : ['powerpoint', '2013', 'sp1'],
        			'version' : None,
        			'razr' : None
				}
			)
		self.assertEqual(
				markup('.net framework 3.5'),
				{
					'keywords' : ['.net', 'framework'],
        			'version' : '3.5',
        			'razr' : None
				}
			)

if __name__ == '__main__':
	main()