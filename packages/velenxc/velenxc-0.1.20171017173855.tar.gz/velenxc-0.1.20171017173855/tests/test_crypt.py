import unittest

from velenxc.crypt import Crypt, ChineseCoding


class CryptTestCase(unittest.TestCase):
    def test_md5_should_return_correctly_even_if_input_is_incorrect(self):
        crypt = Crypt()
        self.assertEqual(len(crypt.md5('我们都是牛人'.encode())), 32)

    def test_md5_should_return_utf8_str(self):
        crypt = Crypt()
        payload = '123456'
        md5_result = crypt.md5(payload)
        md5_result_utf8 = crypt.md5(payload.encode('utf-8').decode('utf-8'))
        self.assertEqual(md5_result, md5_result_utf8)

    def test_md5_should_return_only_utf8_str(self):
        crypt = Crypt()
        payload = '中文'
        md5_result = crypt.md5(payload)
        md5_result_non_utf8 = crypt.md5(payload.encode('big5').decode('big5'))
        self.assertEqual(md5_result, md5_result_non_utf8)

    def test_md5_should_return_256_bits(self):
        crypt = Crypt()
        self.assertEqual(len(crypt.md5('123456556')), 32)
        self.assertEqual(len(crypt.md5('1')), 32)
        self.assertEqual(len(crypt.md5('我们都是牛人！')), 32)


class ChineseCodingTestCase(unittest.TestCase):
    """ Test case """

    def test_check_chinese_return_true(self):
        check_res = ChineseCoding.check_chinese('轻轻的你走了ma')
        check_res2 = ChineseCoding.check_chinese('aaa中 dei()*32')

        self.assertTrue(True in (check_res, check_res2))

    def test_check_chinese_return_false(self):
        check_res = ChineseCoding.check_chinese('womeiyouzhognwen')
        check_res2 = ChineseCoding.check_chinese('123USY weu *(@(@##')

        self.assertTrue(True not in (check_res, check_res2, ))
