import unittest

import unittest
from hw import Numbs

class TestHomework(unittest.TestCase):
    def setUp(self):
        self.data = Numbs()

    def tearDown(self):
        self.data.result=10
        self.data.base_of_data=[]


    def test_delt(self):
        self.data.delt(5,7)
        self.assertEqual(self.data.result, 5-7)

    def test_umn(self):
        self.data.umn(10,12)
        self.assertNotEqual(self.data.result, 10*12)

    def test_trueint(self):
        self.data.sum(5,7)
        self.assertTrue(type(self.data.result) != float)

    def test_divint(self):
        self.data.div(5,7)
        self.assertFalse(type(self.data.result)==int)

    def test_summ(self):
        self.data.sum(5,7)
        self.assertIs(self.data.result,self.data.mult(5,7))

    def test_notdivis(self):
        self.data.div(16,4)
        self.assertIsNot(self.data.result,self.data.sum(16,4))

    def test_is_not_none(self):
        self.data.delt(1804,1506)
        self.assertIsNotNone(self.data.result)

    def test_is_none(self):
        self.assertIsNone(self.data.result)

    def test_baseresult(self):
        self.data.div(35,7)
        self.data.create_base_of_data()
        self.assertIn(self.data.result,self.data.base_of_data)

    def test_is_empty_base(self):
        self.assertNotIn(self.data.result,self.data.base_of_data)

    def test_int(self):
        self.data.umn(100, 4)
        self.assertIsInstance(self.data.result,int)

    def test_floatnt(self):
        self.data.div(100, 4)
        self.assertNotIsInstance(self.data.result,int)



if __name__ == '__main__':
    unittest.main()


