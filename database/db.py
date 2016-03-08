from pymongo import MongoClient
from sampledata import Sampledata


'''
responsible for getting the questions and responses from DB
a question is: { id: int, text: string, conv_id: int}
a response is : { id: int, text: string, conv_id: int, response_to: [{id: int}, {id: int} ]}
'''

class Db:
    env = 'prod'
    client = MongoClient()
    # client = MongoClient("mongodb://mongodb0.example.net:55888")
    questions = []
    responses = []
    conversations = []
    sampledata = Sampledata()

    def __init__(self):
        if self.env == 'prod':
            self.db = self.client.prod
        else:
            self.db = self.client.test

    def getQuestions(self):
        # cursor =  self.db.questions.find().sort({'conv_id': 1, 'q_nr' : 1})
        cursor =  self.db.questions.find().sort([('conv_id', 1), ('q_nr', 1)])
        for document in cursor:
            self.questions.append(document)
        print 'nr of questions: ', len(self.questions)
        return self.questions

    def getResponses(self):
        # cursor = self.db.responses.find().sort({'conv_id': 1, 'r_nr' : 1})
        cursor = self.db.responses.find().sort([('conv_id', 1), ('q_nr', 1)])
        for document in cursor:
            self.responses.append(document)
        print 'nr of responses: ', len(self.responses)
        return self.responses

    def getConversations(self):
        cursor = self.db.convsersations.find()
        for document in cursor:
            self.conversations.append(document)
        return self.conversations

    def _clearQuestions(self):
        cursor = self.db.questions.drop()
        return True

    def _clearResponses(self):
        cursor = self.db.responses.drop()
        return True

    def _clearConvsations(self):
        cursor = self.db.conversations.drop()
        return True

    def _clearDb(self):
        try:
            self._clearQuestions()
            self._clearResponses()
            self._clearConvsations()
            return True
        except Exception, e:
            print e
            return False

    def insertTestData(self):
        testquestions = self.sampledata.getQuestions()
        testresponses = self.sampledata.getResponses()
        testconvs = self.sampledata.getConversations()
        print 'inserting...'
        self.db.questions.insert(testquestions)
        self.db.responses.insert(testresponses)
        self.db.conversations.insert(testconvs)

    def resetDBToTestState(self):
        print 'resetting...'
        self._clearDb()
        self.insertTestData()
