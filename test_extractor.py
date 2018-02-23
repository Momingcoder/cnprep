#!/usr/bin/python
# -*-coding:utf-8-*-

import unittest

from cnprep.extractor import Extractor

class ExtractorTestCase(unittest.TestCase):
    """
    test for Extractor
    """

    def test_init_and_reset_param(self):
        self.assertIsInstance(Extractor(), object)
        ext = Extractor()
        self.assertIsInstance(ext.reset_param(['web', 'telephone']), object)

    def test_url(self):
        msg = '谷歌https://www.google.com/推特\
                https://twitter.com/非死不可wWw.facebook.com'
        ext = Extractor(['url'])
        self.assertEqual(ext.extract(msg)['url'],
                        ['https://www.google.com/',
                        'https://twitter.com/',
                        'wWw.facebook.com'])

    def test_QQ(self):
        msg = '16548425或者1994 or 16841654648431'
        ext = Extractor(['QQ'])
        self.assertEqual(ext.extract(msg)['QQ'],
                        ['16548425'])

    def test_wechat(self):
        msg = 'wechat:weixin2000 or 一些 like this 微信号：wei2016xin'
        ext = Extractor(['wechat'])
        self.assertEqual(ext.extract(msg)['wechat'],
                        ['weixin2000', 'wei2016xin'])

    def test_telephone(self):
        msg = '手机号155-1555-5515或者154 4567 1234也许11121211212'
        ext = Extractor(['telephone'])
        self.assertEqual(ext.extract(msg)['telephone'],
                        ['15515555515', '15445671234'])

    def test_email(self):
        msg = '一般的abc@gmail.com 二班的123 at email.edu.cn \
                没有 call me at there 或者 123 At yahoo Dot cn'
        ext = Extractor(['email'])
        self.assertEqual(ext.extract(msg)['email'],
                        ['abc@gmail.com',
                        '123 at email.edu.cn',
                        '123 At yahoo Dot cn'])

    def test_tex(self):
        msg = '$$e^{i\pi}+1=0$$被称为最美公式，一般的也有$\lambda=\sum_ix_i$'
        ext = Extractor(['tex'])
        self.assertEqual(ext.extract(msg)['tex'],
                        ['$$e^{i\pi}+1=0$$', '$$\lambda=\sum_ix_i$$'])

    def test_emoji(self):
        msg = '\U00010000\U00010001'
        ext = Extractor(['emoji'])
        self.assertEqual(ext.extract(msg)['emoji'],
                        ['\U00010000', '\U00010001'])

    def test_blur(self):
        msg = '吾儿要溜，其实Ⅷ⑦'
        ext = Extractor(['blur'])
        self.assertEqual(ext.extract(msg)['blur'],
                        ['521671087'])

    def test_combination(self):
        msg = '给你一个网址\
                https://123456789?tel=15512345678?wechat=weixin1234。\
                再来个邮箱什么的abc123[at]email.com，留个QQ:123456，\
                午起罢溜司儿。都开始用微信了weiwei_xinxin。找不到就打电话\
                400-800-8888'
        ext = Extractor(['blur', 'wechat', 'url', 'email', 'QQ'])
        self.assertEqual(ext.extract(msg),
                {
                    'email': ['abc123[at]email.com'],
                    'QQ': ['123456'],
                    'wechat': ['weiwei_xinxin'],
                    'url': ['https://123456789?tel=15512345678?wechat=weixin1234'],
                    'blur': ['578642'],
                })


if __name__ == '__main__':
    unittest.main()
