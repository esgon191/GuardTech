from unittest import TestCase, main
from compare import rate_match

class RateMatchTest(TestCase):
	def test_keywords(self):
		self.assertEqual(2, rate_match(['windows', '21h1'], ['windows', '21h1'], 'keywords'))

		self.assertEqual(1, rate_match(['windows', '21h1'], ['windows', '21h1', 'sp1'], 'keywords'))

		self.assertEqual(0, rate_match(['windows', '21h1'], ['windows', '7', 'sp1'], 'keywords'))
	
	def test_razr(self):
		self.assertEqual(2, rate_match('64', '64', 'razr'))

		self.assertEqual(1, rate_match('64', None, 'razr'))

		self.assertEqual(0, rate_match('64', '32', 'razr'))

	def test_versions_single(self):
		self.assertEqual(2, rate_match(['16.2'], ['16.1', '16.2'], 'versions'))

		self.assertEqual(0, rate_match(['16.3'], ['16.1', '16.2'], 'versions'))

		self.assertEqual(2, rate_match(['16.2.3'], ['16.1.0', '16.2.3'], 'versions'))

		self.assertEqual(0, rate_match(['16.3.3'], ['16.1.1', '16.3.3.4'], 'versions'))

	def test_versions_multi(self):
		self.assertEqual(2, rate_match(['16.5'], ['16.1', '16.2', ('16.4', '16.6')], 'versions')) 

		self.assertEqual(2, rate_match(['16.5'], ['16.1', '16.2', ('16.4', '16.6.5')], 'versions')) 

		self.assertEqual(2, rate_match(['16.10'], ['16.1', '16.2', ('16.4', '16.6'), ('16.8', '16.12')], 'versions'))

		self.assertEqual(2, rate_match(['16.5.5'], ['16.1', '16.2', ('16.3', '16.6')], 'versions')) 

		self.assertEqual(0, rate_match(['16.5'], ['16.1', '16.2', ('16.3', '16.4')], 'versions')) 

		self.assertEqual(0, rate_match(['16.5.5'], ['16.1', '16.2', ('16.3', '16.5')], 'versions')) 


if __name__ == '__main__':
	main()