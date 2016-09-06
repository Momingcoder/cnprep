#!/usr/bin/python
# -*-coding:utf-8-*-

"""
convert Chinese to numbers
"""

import re
# chinese_character_pattern = re.compile(ur"([\u4e00-\u9fa5]+)")
# CCP = chinese_character_pattern

from xpinyin import Pinyin
pinyin = Pinyin()

special_char = {
    # Roman
    u'Ⅰ': 1,
    u'Ⅱ': 2,
    u'Ⅲ': 3,
    u'Ⅳ': 4,
    u'Ⅴ': 5,
    u'Ⅵ': 6,
    u'Ⅶ': 7,
    u'Ⅷ': 8,
    u'Ⅸ': 9,
    # with circle
    u'①': 1,
    u'②': 2,
    u'③': 3,
    u'④': 4,
    u'⑤': 5,
    u'⑥': 6,
    u'⑦': 7,
    u'⑧': 8,
    u'⑨': 9,
    # others
    u'〇': 0,
}

pinyin2number = {
    u'ling': 0,
    u'yao': 1,
    u'yi': 1,
    u'er': 2,
    u'san': 3,
    u'si': 4,
    u'wu': 5,
    u'liu': 6,
    u'qi': 7,
    u'ba': 8,
    u'jiu': 9,
}


# def extract_chinese(buf):
#     """
#       extract chinese characters
#     """
#     segment_list = []
#     m = CCP.search(buf)
#     while m is not None:
#         segment = m.group(1)
#         segment_list.append(segment)
#         idx = m.start() + len(segment)
#         buf = buf[idx:]
#         m = CCP.search(buf)

#     return segment_list

def get_number(message, limit=4):
    """
    convert Chinese to pinyin and extract useful numbers

    attention:
        1. only for integer
        2. before apply this method, the message should be preprocessed

    input:
        message: the message you want to extract numbers from.
        limit: limit the length of number sequence
    """
    words = pinyin.get_pinyin(message).split('-')
    numbers = []
    tmp = ''
    count = 0
    for w in words:
        if re.search(r'\w', w) is None:
            for s in list(w):
                if s in special_char.keys():
                    count += 1
                    tmp += str(special_char[s])
                else:
                    if count >= limit:
                        numbers.append(tmp)
                    count = 0
                    tmp = ''
        elif w in pinyin2number.keys():
            count += 1
            tmp += str(pinyin2number[w])
        else:
            if count >= limit:
                numbers.append(tmp)
            count = 0
            tmp = ''
    if count >= limit:
        numbers.append(tmp)
    return numbers