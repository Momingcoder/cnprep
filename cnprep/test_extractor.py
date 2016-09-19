#!/usr/bin/python
# -*-coding:utf-8-*-

import unittest

from extractor import Extractor

class ExtractorTestCase(unittest.TestCase):
    """
    test for Extractor
    """

    def test_init_and_reset_param(self):
        self.assertIsInstance(Extractor(), object)
        ext = Extractor()
        self.assertIsInstance(ext.reset_param(['web', 'telephone']), object)

    def test_url(self):
        msg = u'谷歌https://www.google.com/推特\
                https://twitter.com/非死不可www.facebook.com'
        ext = Extractor(['url'])
        self.assertEqual(ext.extract(msg)['url'],
                        [u'https://www.google.com/',
                        u'https://twitter.com/',
                        u'www.facebook.com'])

    def test_QQ(self):
        msg = u'16548425或者1994 or 16841654648431'
        ext = Extractor(['QQ'])
        self.assertEqual(ext.extract(msg)['QQ'],
                        [u'16548425'])

    def test_wechat(self):
        msg = u'wechat:weixin2000 or 一些 like this 微信号：wei2016xin'
        ext = Extractor(['wechat'])
        self.assertEqual(ext.extract(msg)['wechat'],
                        [u'weixin2000', u'wei2016xin'])

    def test_telephone(self):
        msg = u'手机号155-1555-5515或者154 4567 1234也许11121211212'
        ext = Extractor(['telephone'])
        self.assertEqual(ext.extract(msg)['telephone'],
                        [u'15515555515', u'15445671234'])

    def test_email(self):
        msg = u'一般的abc@gmail.com 二班的123 at email.edu.cn \
                没有 call me at there'
        ext = Extractor(['email'])
        self.assertEqual(ext.extract(msg)['email'],
                        [u'abc@gmail.com', u'123 at email.edu.cn'])

    def test_tex(self):
        msg = u'$$e^{i\pi}+1=0$$被称为最美公式，一般的也有$\lambda=\sum_ix_i$'
        ext = Extractor(['tex'])
        self.assertEqual(ext.extract(msg)['tex'],
                        [u'$$e^{i\pi}+1=0$$', u'$$\lambda=\sum_ix_i$$'])

    def test_emoji(self):
        msg = u'\U00010000\U00010001'
        ext = Extractor(['emoji'])
        self.assertEqual(ext.extract(msg)['emoji'],
                        [u'\U00010000', u'\U00010001'])

    def test_blur(self):
        msg = u'吾儿要溜，其实Ⅷ⑦'
        ext = Extractor(['blur'])
        self.assertEqual(ext.extract(msg)['blur'],
                        [u'521671087'])

    def test_combination(self):
        msg = u'给你一个网址\
                https://123456789?tel=15512345678?wechat=weixin1234。\
                再来个邮箱什么的abc123[at]email.com，留个QQ:123456，\
                午起罢溜司儿。都开始用微信了weiwei_xinxin。找不到就打电话\
                400-800-8888'
        ext = Extractor(['blur', 'wechat', 'url', 'email', 'QQ'])
        self.assertEqual(ext.extract(msg),
                {
                    'email': [u'abc123[at]email.com'],
                    'QQ': [u'123456'],
                    'wechat': [u'weiwei_xinxin'],
                    'url': [u'https://123456789?tel=15512345678?wechat=weixin1234'],
                    'blur': [u'578642'],
                })


if __name__ == '__main__':
    unittest.main()
