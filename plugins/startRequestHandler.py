#!/usr/bin/python
# -*- coding: utf-8 -*-
#Simplified Chinese localization: Linus Yang <laokongzi@gmail.com>

import re

from plugin import *
from plugin import __criteria_key__

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.systemObjects import DomainObject, ResultCallback
from siriObjects.websearchObjects import WebSearch

webSearchAnswerText = {"de": u"Das Web nach {0} durchsuchen …", "en": u"Searching the web for {0} …", "fr": u"Searching the web for {0} …", "zh": u"正在搜索 {0} …"}
webSearchAnswerFailureText = {"de": u"Entschuldigung, Ich, ich kann jetzt nicht das Web durchsuchen.", "en": u"Sorry but I cannot search the web right now.", "fr": u"Sorry but I cannot search the web right now.", "zh": u"抱歉我现在无法搜索网页。"}
class startRequestHandler(Plugin):    

    #we should provide a shortcut for this....
    @register("de-DE", u"\^webSearchQuery\^=\^([a-z, ]+)\^\^webSearchConfirmation\^=\^([a-z]+)\^")     
    @register("en-US", u"\^webSearchQuery\^=\^([a-z, ]+)\^\^webSearchConfirmation\^=\^([a-z]+)\^")
    @register("en-AU", u"\^webSearchQuery\^=\^([a-z, ]+)\^\^webSearchConfirmation\^=\^([a-z]+)\^")
    @register("en-GB", u"\^webSearchQuery\^=\^([a-z, ]+)\^\^webSearchConfirmation\^=\^([a-z]+)\^")
    @register("fr-FR", u"\^webSearchQuery\^=\^([a-z, ]+)\^\^webSearchConfirmation\^=\^([a-z]+)\^")
    @register("zh-CN", u"(?u)\^webSearchQuery\^=\^([\w ]+)\^\^webSearchConfirmation\^=\^([\w]+)\^")
    def webSearchConfirmation(self, speech, language):
        regMatched = re.match(u"(?u)\^webSearchQuery\^=\^([\w ]+)\^\^webSearchConfirmation\^=\^([\w]+)\^", speech, re.IGNORECASE)
        if regMatched != None:
            webSearchQuery = regMatched.group(1)
            webSearchConfirmation = regMatched.group(2)
        
        lang = language.split("-")[0]

        resultCallback1View = AddViews(refId="", views=[AssistantUtteranceView(dialogIdentifier="WebSearch#initiateWebSearch", text=webSearchAnswerText[lang].format(u"“{0}”".format(webSearchQuery)), speakableText=webSearchAnswerText[lang].format(webSearchQuery))])
        
        search = WebSearch(refId="", aceId="", query=webSearchQuery)
        resultCallback3View = AddViews(refId="", views=[AssistantUtteranceView(dialogIdentifier="WebSearch#fatalResponse", text=webSearchAnswerFailureText[lang], speakableText=webSearchAnswerFailureText[lang])])
        resultCallback3 = ResultCallback(commands=[resultCallback3View])
        search.callbacks = [resultCallback3]

        resultCallback2 = ResultCallback(commands=[search])
        resultCallback1View.callbacks = [resultCallback2]

        self.complete_request(callbacks=[ResultCallback(commands=[resultCallback1View])])
    