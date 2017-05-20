# -*- coding: utf-8 -*-
import re

_matches = lambda url, r: r.search(url)


r = re.compile('.*\/\d+\/\d+.shtml')

print (_matches('http://news.uuu9.com/tfxw/201611/396718.shtml',r))