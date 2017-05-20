# -*- coding: utf-8 -*-
import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_datetime(str):
    def match_res(reg, str):
        match_obj = re.match(reg, str)
        if match_obj:
            return match_obj.group(1)

    _str = match_res(r"(\d+-\d+-\d+( \d+:\d+:\d+)?)", str)
    # _str = re.findall(r"(\d+-\d+-\d+ (\d+:\d+:\d+))", str)
    return _str

if __name__ == "__main__":
    print (get_datetime('2017-2-24 11:11:11萨克的国家傻大个'))