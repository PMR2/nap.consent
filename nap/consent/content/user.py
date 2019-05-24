from nap.consent import _
from time import time
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
import random
from BTrees.OOBTree import OOBTree
from .session import Session

class User(Implicit, Persistent, RoleManager, Item):
    
    def __init__(self,userId):
        self._userId = userId
        self._sessions = OOBTree()
        self._totFeedback = 0
        self._answered = set()
        
    def addAnswer(self, sessionId, questionId, answer, nav, time, context, loginStatus, page, query):
        if self._sessions.has_key(sessionId):
            session = self._sessions[sessionId]
        else:
            session = Session(sessionId)
            self._sessions[sessionId] = session
        addIsSuccess = session.addAnswer(questionId, answer, nav, time, context, loginStatus, page, query)
        self._totFeedback += 1 if addIsSuccess else 0
        self._answered.add(questionId)
        return addIsSuccess
    
    def getTotFeedback(self, **kwargs):
        if len(kwargs) is 0:
            return self._totFeedback
        else:
            sessionId = kwargs['sessionId']
            if self._sessions.has_key(sessionId):
                session = self._sessions[sessionId]
                return session.getTotFeedback()
        return 0
    
    def getTotSession(self):
        return len(self._sessions)
    
    #isAnswered(questionId, sessionId=sessionId, context=context)
    def isAnswered(self, questionId, **kwargs):
        #note: isAnswered(questionId)
        if len(kwargs) is 0:
            return True if questionId in self._answered else False
        #note: isAnswered(questionId, sessionId=sessionId, context=context) or
        #note: isAnswered(questionId, sessionId=sessionId)
        else:
            sessionId = kwargs['sessionId']
            if self._sessions.has_key(sessionId):
                session = self._sessions[sessionId]
                return session.isAnswered(questionId, **kwargs)
        return False
    
    def getAnswers(self):
        return self._answered