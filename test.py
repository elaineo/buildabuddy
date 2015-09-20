from app import app
import unittest


class MainTestCase(unittest.TestCase):

    def test_data(self):
        self.assertEqual(200, 200)


if __name__ == '__main__':
    unittest.main()
