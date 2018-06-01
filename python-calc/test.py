import unittest
import calc

class TestCalc(unittest.TestCase):

	def setUp(self):
        	self.cases = [
			'7 + 2',
			'8/3',
			'3 divided by 0',
			'twenty one times 2',
			'1232+13123*8989/89899*465465+54646*789798/465456',
			'3+3-12312/123123-32424234234*123123123+5+43+122+423+5/23+23+234+123+123+123-32132/2+21/123/123123/123123/312312',
			'1+3-4',
			'one thousand two hundred fifty three * one million / two - forty four',
			'three million two thousand fifty one / 33 + eleven million - twenty nine',
		]

	def test_get_terms(self):
		'''
			Test if we can get 2 terms properly to proceed with operation
		'''
		#-- Case 1+3-4
		self.assertEqual(calc.get_terms(string=self.cases[6], position=3),('3','4',False))

		#-- Case 1232+13123*8989/89899*465465+54646*789798/465456
		self.assertEqual(calc.get_terms(string=self.cases[4], position=10),('13123','8989','/'))
		

	def test_calc(self):
		'''
			Check if calculator can performe 4 basic operations properly 
		'''
		self.assertEqual(calc.calc('+','1','1'), 2)
		self.assertEqual(calc.calc('-','11','111'), -100)
		self.assertEqual(calc.calc('*','11','11'), 121)
		self.assertEqual(calc.calc('/','33','3'), 11)
		self.assertRaises(ZeroDivisionError, calc.calc, '/','33','0')


	def test_run(self):
		'''
			Validate calculation in a long string 
		'''
		#-- Case 1232+13123*8989/89899*465465+54646*789798/465456
		self.assertEqual(calc.run(string=self.cases[4]), 610784036)

		#-- Case 3+3-12312/123123-32424234234*123123123+5+43+122+423+5/23+23+234+123+123+123-32132/2+21/123/123123/123123/312312
		self.assertEqual(calc.run(string=self.cases[5]), -3992172979773607623)

	def test_normalize_number(self):
		'''
			Validate normalization from words to numbers
		'''
		#-- Case one thousand two hundred fifty three * one million / two - forty four
		self.assertEqual(calc.normalize_numbers(line=self.cases[7]), '1253*1000000/2-44')

		#-- Case three million two thousand fifty one / 33 + eleven million - twenty nine
		self.assertEqual(calc.normalize_numbers(line=self.cases[8]), '3002051/33+11000000-29')

if __name__ == '__main__':
    unittest.main()
