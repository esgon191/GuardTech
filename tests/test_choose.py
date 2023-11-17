from unittest import TestCase, main
import sys, logging
sys.path.insert(1, '../')
from compare import choose
from exceptions import *

logging.basicConfig(filename='compare.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
'''
logger = logging.getLogger()
sys.stdout = open('compare.log','w')
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
'''
class ChooseTest(TestCase):
    def test_without_platform(self):
        self.assertEqual(
            choose('CVE-2022-26901', 'Microsoft Windows - Windows 10 version 21H1 ProfessionalWorkstation (x64)', 'Microsoft Office - 2013 SP1 - C:\\Program Files (x86)\\Microsoft Office\\Office15\\'),
            'https://www.microsoft.com/downloads/details.aspx?familyid=1755810a-893f-4627-b4ef-54687f8d8896'
        )

    def test_with_platform(self):
        self.assertEqual(
            choose('CVE-2016-3255', 'Microsoft Windows - Windows 10 version 21H1 ProfessionalWorkstation (x64)', 'Microsoft .NET Framework - 3.5'),
            'https://catalog.update.microsoft.com/v7/site/Search.aspx?q=KB3163912'
        )

    def test_non_microsoft_developer(self):
        with self.assertRaises(NotImplementedError) as ex:
            choose('CVE-2016-3255', 'Shit ass crack', 'heroine los angeles')

    def test_no_matching_link_obvious(self):
        with self.assertRaises(NoMatchingLink) as ex:
            choose('CVE-2016-3255', 'microsoft shit ass crack', 'microsoft heroine los angeles')


if __name__ == "__main__":
    main()
