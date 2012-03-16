#!/usr/bin/python
# -*- coding: utf-8 -*-
# Google units calculator v1.0
# by Mike Pissanos (gaVRos) 
#    Usage: simply say Convert or Calculate X to Y
#    Examples: 
#             Convert 70 ferinheight to celsius 
#             Convert 1 euro to dollars
#             Convert 1 tablespoon to teaspoons
#             Calculate 30 divided by 10   


import re
import urllib2, urllib
import json

from plugin import *
from plugin import __criteria_key__

from siriObjects.uiObjects import AddViews
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class UnitsConverter(Plugin):
    
    @register("en-US", "(convert|calculate)* ([\w ]+)")
    @register("en-GB", "(convert|calculate)* ([\w ]+)")
    @register("zh-CN", u"(计算|转换|换算)([\w ]+)")
    def defineword(self, speech, language, regex):
        Title = regex.group(regex.lastindex)
        Query = urllib.quote_plus(Title.encode("utf-8"))
        SearchURL = u'http://www.google.com/ig/calculator?q=' + str(Query)
        try:
            result = urllib2.urlopen(SearchURL).read().decode("utf-8", "ignore")
            result = re.sub("([a-z]+):", '"\\1" :', result)
            result = json.loads(result)
            ConvA = result['lhs']
            ConvB = result['rhs'] 
            if language == 'zh-CN':
                self.say(u"这是我得到的结果…" '\n' +str(ConvA.encode("utf-8")) + " 等于 " +str(ConvB.encode("utf-8")))
            else:
                self.say("Here is what I found..." '\n' +str(ConvA) + " equals, " +str(ConvB))
            self.complete_request()
        except (urllib2.URLError):
            if language == 'zh-CN':
                self.say(u"抱歉，我无法连接到谷歌的计算服务。")
            else:
                self.say("Sorry, but a connection to the Google calculator could not be established.")
            self.complete_request()
