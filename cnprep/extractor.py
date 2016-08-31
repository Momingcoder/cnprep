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
    
    def __init__(self, delete=False, args=[], blur=False, limit=4):
        """
        delete: delete the found info except blur
        args: option
            e.g. ['email', 'number']
        blur: convert Chinese to pinyin and extract useful numbers
        limit: parameter for get_number
        """
        self._delete = delete
        self._blur = blur
        self._limit = limit
        self.m = ''
        self._email = []
        self._number = {}
        self._web_addr = []
        self._emoji = []
        self._tex = []

        if isinstance(args, list):
            self.option = args
        elif isinstance(args, str):
            self.option = [x.strip() for x in args.split(',')]
        else:
            self.option = []
            print('Input error. Only delete the punctuation.')

    def reset_param(self, delete=False, args=[], blur=False, limit=4):
        self._delete = delete
        self._blur = blur
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
            'number': self._number,
            'web': self._web_addr,
            'emoji': self._emoji,
            'tex': self._tex,
        }

        for item in self.option:
            info[item] = self.options2attr[item]
        return (self.m, info)

    def extract(self, m):
        """
        extract info specified in option
        """
        self.m = m
        self._preprocess()

        self.options2func = {
            'email': self._email_filter(),
            'number': self._number_filter(),
            'web': self._web_filter(),
            'emoji': self._emoji_filter(),
            'tex': self._tex_filter(),
        }

        for func in self.option:
            self.options2func[func]
        self._filter()
        if self._blur:
            self._number['blur'] = get_number(self.m, self._limit)
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
        self._email = re.findall(r'[\w\.-]+@[\w\.-]+', self.m)
        if self._delete and self._email != []:
            self.m = re.sub(r'[\w\.-]+@[\w\.-]+', '', self.m)
        # @ => at
        others = re.findall(r'[\w\.-]+\s?at\s?[\w\.-]+', self.m)
        if self._delete and others != []:
            self.m = re.sub(r'[\w\.-]+\s?at\s?[\w\.-]+', '', self.m)
        for i in range(len(others)):
            others[i] = re.sub(r'\s?at\s?', '@', others[i])
        self._email.extend(others)
        # @ => @@
        others = re.findall(r'[\w\.-]+@@[\w\.-]+', self.m)
        if self._delete and others != []:
            self.m = re.sub(r'[\w\.-]+@@[\w\.-]+', '', self.m)
        for i in range(len(others)):
            others[i] = re.sub(r'@@', '@', others[i])
        self._email.extend(others)

    def _number_filter(self):
        # usually 4 or more
        # telephone: xxx-xxxx-xxxx
        seg = re.findall(r'(\d{3})[-\s]?(\d{4})[-\s]?(\d{4})', self.m)
        if self._delete and seg != []:
            self.m = re.sub(r'(\d{3})[-\s]?(\d{4})[-\s]?(\d{4})', '', self.m)
        for index in range(len(seg)):
            seg[index] = ''.join(list(seg[index]))
        self._number['telephone'] = seg
        # others (maybe QQ or something)
        self._number['QQ'] = re.findall(r'\d{5,10}', self.m)
        if self._delete and self._number['QQ'] != []:
            self.m = re.sub(r'\d{5,10}', '', self.m)

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