"""
@author: 伟佳
@desc: 暴力匹配分词, 根据 config.SKILL_PATH 所在的词典作为参考
"""

import abc
import os
import re
from config import SKILL_PATH


class BaseTokenizer(object):
    """Base class for tokenizer"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, skill_path, **kwargs):
        if isinstance(skill_path, str):
            if os.path.isfile(skill_path):
                print("skill_path: ", skill_path)
                skills = [skill.strip().lower() for skill in
                          open(skill_path, 'r').readlines() if skill.strip()]
            else:
                raise ValueError(
                    "specified skill file does not exist", skill_path)
        elif isinstance(skill_path, list) or isinstance(skill_path, set):
            skills = [skill.strip().lower() for skill in list(
                set(skill_path)) if skill.strip()]
        else:
            raise ValueError(
                'BaseTokenizer only accept str as skill_path, cannot use type',
                type(skill_path))
        self.skills = set(skills)

    @abc.abstractmethod
    def cut(self, text: str):
        """tokenize a string"""
        pass


class MatchTokenizer(BaseTokenizer):

    def __init__(self, skill_path=SKILL_PATH, separate_length=4):
        super(self.__class__, self).__init__(skill_path=skill_path)
        self.dict_long = set(
            [s for s in self.skills if len(s) > separate_length])
        self.dict_short = self.skills - self.dict_long
        print('long dict has %s words, short dict has %s words' %
              (len(self.dict_long), len(self.dict_short)))

    def cut(self, text):
        """returns a list of words"""
        if not isinstance(text, str):
            return ['']
        return self.convert_text_str_all(text, output='list')

    @staticmethod
    def _match_replace(text, title_word, remove_short):
        if not isinstance(text, str):
            return ''
        finish_intervals = []
        res = []
        min_l, max_l = min(map(len, title_word)), max(map(len, title_word))
        text_l = len(text)
        for length in range(max_l, min_l - 1, -1):
            for index in range(text_l + 1 - length):
                if text[index: index + length] in title_word:
                    term = text[index: index + length]
                    if re.match('^[a-z]{0,3}$', term):
                        if index != 0:
                            if re.match('[a-z_-]', text[index - 1]):
                                continue
                        if index + length != text_l:
                            if re.match('[a-z_-]', text[index + length]):
                                continue
                    if remove_short:
                        flag = False
                        for finish in finish_intervals:
                            if index >= finish[0] and index + length <= finish[1]:
                                flag = True
                                break
                        if not flag:
                            res.append(term)
                            finish_intervals.append((index, index + length))
                    else:
                        res.append(term)
        return res

    @staticmethod
    def _match_long_words(text, title_word):
        res = []
        for t in title_word:
            if t in text:
                w = text.count(t)
                res += w * [t]
        return res

    def convert_text_str(self, text, output='str'):
        """
        eg: 熟练使用javascript ==> javascript
        returns a string with matched words joined by blank spaces
        """
        if not isinstance(text, str):
            return ''
        text = text.lower()
        res = self._match_replace(text, self.dict_short, remove_short=True)
        res_long = self._match_long_words(text, self.dict_long)
        res = res + res_long
        if output == 'str':
            return ' '.join(res)
        else:
            return res

    def convert_text_str_all_old(self, text, output='str'):
        """
        eg: 熟练使用javascript ==> javascript, java
        returns a string with matched words joined by blank spaces
        """
        if not isinstance(text, str):
            return ''
        text = text.lower()
        res = self._match_replace(text, self.dict_short, remove_short=False)
        res_long = self._match_long_words(text, self.dict_long)
        res = res + res_long
        if output == 'str':
            return ' '.join(res)
        else:
            return res

    def convert_text_str_all(self, text, output='str'):
        """
        eg: 熟练使用javascript ==> javascript, java
        returns a string with matched words joined by blank spaces
        """
        if not isinstance(text, str):
            return ''
        text = text.lower()
        res = self._match_backwards(text, self.skills)
        if output == 'str':
            return ' '.join(res)
        else:
            return res

    @staticmethod
    def _match(text, title_word):
        res = []
        min_l, max_l = min(map(len, title_word)), max(map(len, title_word))
        i = 0
        while i < len(text) - min_l:
            flag = False
            for length in range(max_l, min_l - 1, -1):
                tmp = text[i: i + length].lower()
                if re.match(u"[\u4e00-\u9fa5]+[a-z]{1,3}$", tmp):
                    continue
                if tmp in title_word:
                    res.append(tmp)
                    i = i + len(tmp)
                    flag = True
                    break
            if not flag:
                i += 1
        return res

    @staticmethod
    def _match_backwards(text, title_word):
        res = []
        min_l, max_l = min(map(len, title_word)), max(map(len, title_word))
        i = len(text)
        while i >= min_l:
            flag = False
            for length in range(max_l, min_l - 1, -1):
                tmp = text[i - length: i].lower()
                if re.match(u"[\u4e00-\u9fa5]+[a-z]{1,3}$", tmp):
                    continue
                if tmp in title_word:
                    res.append(tmp)
                    i = i - len(tmp)
                    flag = True
                    break
            if not flag:
                i -= 1
        res.reverse()
        return res


if __name__ == '__main__':
    tokenizer = MatchTokenizer()
    while True:
        inp = input('>> ')
        print(tokenizer.cut(inp))
