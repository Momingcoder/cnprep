#!/usr/bin/python
# -*-coding:utf-8-*-

"""
basic class
"""

import re

from zh2num import get_number

class Extractor(object):
    """
    1. default delete the punctuation
    2. extract e-mail, telephone number, web address, etc.
    3. the info extracted is keeped if delete is false (default)

    init:
        option: ['xxx', 'yyy'] or 'xxx, yyy'

    input:
        one line string
    
    output:
        (string, {info})
    """
    
    def __init__(self, delete=False, args=[], limit=4):
        """
        delete: delete the found info except blur
        args: option
            e.g. ['email', 'number']
        blur: convert Chinese to pinyin and extract useful numbers
        limit: parameter for get_number
        """
        self._delete = delete
        self._limit = limit
        self.m = ''
        self._email = []
        self._telephone = []
        self._QQ = []
        self._wechat = []
        self._web_addr = []
        self._emoji = []
        self._tex = []
        self._blur = []

        if isinstance(args, list):
            self.option = args
        elif isinstance(args, str):
            self.option = [x.strip() for x in args.split(',')]
        else:
            self.option = []
            print('Input error. Only delete the punctuation.')

    def reset_param(self, delete=False, args=[], limit=4):
        self._delete = delete
        self._limit = limit
        if isinstance(args, list):
            self.option = args
        elif isinstance(args, str):
            self.option = [x.strip() for x in args.split(',')]
        else:
            self.option = []
            print('Input error. Only delete the punctuation.')
        
    def _get_result(self):
        """
        get the result
        """
        info = {}

        self.options2attr = {
            'email': self._email,
            'telephone': self._telephone,
            'QQ' : self._QQ,
            'wechat': self._wechat,
            'web': self._web_addr,
            'emoji': self._emoji,
            'tex': self._tex,
            'blur': self._blur,
        }

        for item in self.option:
            info[item] = self.options2attr[item]
        return (self.m, info)

    def _clear(self):
        """
        clear attr
        """
        self._email = []
        self._telephone = []
        self._QQ = []
        self._wechat = []
        self._web_addr = []
        self._emoji = []
        self._tex = []
        self._blur = []

    def extract(self, m):
        """
        extract info specified in option
        """
        self._clear()
        self.m = m
        self._preprocess()

        self.options2func = {
            'email': self._email_filter,
            'telephone': self._telephone_filter,
            'QQ' : self._QQ_filter,
            'wechat': self._wechat_filter,
            'web': self._web_filter,
            'emoji': self._emoji_filter,
            'tex': self._tex_filter,
        }

        for func in self.option:
            if func == "blur":
                continue
            self.options2func[func]()
        self._filter()
        if 'blur' in self.option:
            self._blur = get_number(self.m, self._limit)
        return self._get_result()

    def _filter(self):
        """
        delete the punctuation
        """
        pattern = u"[\s+\.\!\-\/_,$%^*(+\"\']+|[+——！】【，。？?:、：~@#￥%……&*“”（）]+"
        self.m = re.sub(pattern, "", self.m)

    def _preprocess(self):
        """
        if the input string is str, try to convert it to unicode
        """
        if not isinstance(self.m, unicode):
            try:
                self.m = unicode(self.m, 'utf-8')
            except e:
                print('Convert to unicode raise error: ' + e)

    def _email_filter(self):
        self._email = re.findall(r'[\w\.-]+@+[\w\.-]+[\.]+[\w\.-]+', self.m)
        if self._delete and self._email != []:
            self.m = re.sub(r'[\w\.-]+@+[\w\.-]+[\.]+[\w\.-]+', '', self.m)
        # @ => at
        others = re.findall(r'[\w\.-]+.?at.?[\w\.-]+[\.]+[\w\.-]+', self.m, re.I)
        if self._delete and others != []:
            self.m = re.sub(r'[\w\.-]+.?at.?[\w\.-]+[\.]+[\w\.-]+', '', self.m, re.I)
        # for i in range(len(others)):
        #     others[i] = re.sub(r'.?at.?', '@', others[i])
        self._email.extend(others)
        # # @ => @@
        # others = re.findall(r'[\w\.-]+@@[\w\.-]+', self.m)
        # if self._delete and others != []:
        #     self.m = re.sub(r'[\w\.-]+@@[\w\.-]+', '', self.m)
        # for i in range(len(others)):
        #     others[i] = re.sub(r'@@', '@', others[i])
        # self._email.extend(others)

    def _telephone_filter(self):
        # telephone: xxx-xxxx-xxxx
        pre = r'(13\d|145|147|15\d|18\d|10\d|12\d|17\d|400|800)'
        pattern = pre + r'[-\s]?(\d{4})[-\s]?(\d{4})'
        seg = re.findall(r'(\d{3})[-\s]?(\d{4})[-\s]?(\d{4})', self.m)
        if self._delete and seg != []:
            self.m = re.sub(r'(\d{3})[-\s]?(\d{4})[-\s]?(\d{4})', '', self.m)
        for index in range(len(seg)):
            seg[index] = ''.join(list(seg[index]))
        self._telephone = seg

    def _QQ_filter(self):
        # maybe QQ or something
        self._QQ = re.findall(r'\d{5,10}', self.m)
        if self._delete and self._QQ != []:
            self.m = re.sub(r'\d{5,10}', '', self.m)

    def _wechat_filter(self):
        # maybe wechat
        pattern = re.compile(u'微信|v信|weixin|wx|wechat')
        mtc = pattern.search(self.m, re.I)
        m = self.m
        seq = []
        wechat_len = 25
        while mtc != None:
            seq.extend(re.findall(r'\w{5,20}', m[max(0, mtc.start()-wechat_len):mtc.start()]))
            seq.extend(re.findall(r'\w{5,20}', m[mtc.end():(mtc.end()+wechat_len)]))
            m = m[mtc.end():]
            mtc = pattern.search(m, re.I)
        if seq != []:
            self._wechat.extend(seq)
            if self._delete:
                for s in self._wechat:
                    self.m = re.sub(s, '', self.m)

    def _web_filter(self):
        # only extract http(s)
        self._web_addr = re.findall(r'(https?://[^\s]+)', self.m)
        if self._delete and self._web_addr != []:
            self.m = re.sub(r'(https?://[^\s]+)', '', self.m)

    def _emoji_filter(self):
        try:
            # UCS-4
            self._emoji = re.findall(u'[\U00010000-\U0010ffff]', self.m)
            if self._delete and self._emoji != []:
                self.m = re.sub(u'[\U00010000-\U0010ffff]', '', self.m)
        except re.error:
            # UCS-2
            self._emoji = re.findall(u'[\uD800-\uDBFF][\uDC00-\uDFFF]', self.m)
            if self._delete and self._emoji != []:
                self.m = re.sub(u'[\uD800-\uDBFF][\uDC00-\uDFFF]', '', self.m)

    def _tex_filter(self):
        # this may look ugly...
        self._tex = re.findall(r'\${1,2}.+?\${1,2}', self.m)
        if self._delete and self._tex != []:
            self.m = re.sub(r'\${1,2}.+?\${1,2}', '', self.m)
        for i in range(len(self._tex)):
            self._tex[i] = re.sub(r'\$+', '$$', self._tex[i])