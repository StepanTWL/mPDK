from unittest import TestCase, main
from main import function_transmit


class Tests_string(TestCase):

    def test_01(self):
        self.assertEqual(function_transmit('[0c], size=8, crc32=true, cycle=true'), b'\x0c\x00\x00\x00\x00\x00\x00\x00\xd9\x35\x72\xcd')

    def test_02(self):
        self.assertEqual(function_transmit('[0c], size=8, crc32=true, cycle=true'), b'\x0c\x00\x00\x00\x00\x00\x00\x00\xd9\x35\x72\xcd')

    """
    def test_error(self):
        with self.assertRaises(ValueError) as e:
            calculator('t+k-l')
        self.assertEqual('text', e.exception.args[0])
"""


if __name__ == 'main':  # if ide not pycharm
    main()
