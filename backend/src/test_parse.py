#!/usr/bin/python3.9
import parse
from parse import TOKEN_NAME 
from parse import TOKEN_LIST
from parse import TOKEN_DUE_DATE
from parse import TOKEN_COUNT
from parse import TOKEN_TYPE
import unittest

class testParse(unittest.TestCase):

    def test_course_tokens(self):
        """
        Example: Given an string of 
        'ENVS 23 or CHEM 1A; ENVS 24 or BIOE 20C; ENVS 25;'
        where each input of the test would be

        'ENVS 23 or CHEM 1A'
        'ENVS 24 or BIOE 20C'
        'ENVS 25'

        Return the tokens of the boolean operands and courses and their
        starting index poistion in the string
        'ENVS 23 or CHEM 1A'
         0123456789...

        'ENVS 23', 0
        'or', 8
        'CHEM 1A', 11

        """
        def convertToList(expr):
            return list(parse.course_tokens(expr))

        self.assertEqual([('ENVS 100', 0), ('and', 9), ('ENVS 100L', 13)], 
                        convertToList('ENVS 100 and ENVS 100L'))

        self.assertEqual([('ENVS 183A', 0)], 
                        convertToList('ENVS 183A'))
        
        self.assertEqual([('ENVS 24', 0), ('or', 8), ('BIOE 20C', 11)], 
                        convertToList('ENVS 24 or BIOE 20C'))
    
        self.assertEqual([('ENVS 24', 0), ('or', 8), ('BIOE 20C', 11)], 
                        convertToList('ENVS 24 or BIOE 20C'))

        self.assertEqual([
                        ('STAT 7', 0),
                        ('and', 7),
                        ('STAT 7L', 11),
                        ('or', 20),
                        ('ECON 113', 23),
                        ('or', 32),
                        ('OCEA 90', 35)
                        ],
                    convertToList('STAT 7 and STAT 7L, or ECON 113 or OCEA 90'))

    def test_num_from_tokens(self):
        """
        Given a prerequiste string of

        'one from: "CSE-101" ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21,
        or ECON-101'

        Parse the string and return

        'one' -> total required = 1
        'CSE-101' -> requirement name = "CSE-101"
        'ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21,
        or ECON-101' -> requirement list -> .
        """
        test = self

        def createDummyTokens(total, name, list, type, due_date):
            return {TOKEN_COUNT: total, TOKEN_NAME: name, 
                    TOKEN_LIST: list, TOKEN_TYPE: type,
                    TOKEN_DUE_DATE: due_date}
        class NumTest:
            def __init__(self, expr):
                self.expr = expr
                self.count = 0
                self.toks = list(parse.num_from_tokens(expr))
                self.length = len(self.toks)

            def testCurrentToken(self, first):
                #If more calls are made than the expected number of matches
                #Then most likely our parser gave less matches than
                #what would wexpect
                test.assertNotEqual(self.count, self.length, 
                            msg='Parser most likely gave less matches than expected')
                if self.count < self.length:
                    test.assertDictEqual(first, self.toks[self.count])
                self.count = self.count + 1
                


        simpleNumList = NumTest('one from: ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21, PHIL 22, PHIL 24, PHIL 28,\
 or PHIL 80G')

        
        simpleNumList.testCurrentToken(
            createDummyTokens(
            total=1, 
            name=None, 
            list='ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21, PHIL 22, \
PHIL 24, PHIL 28, or PHIL 80G',
            type=None,
            due_date = None))

        simpleNumList = NumTest(
'two from: "req_name test" CSE 130A, random string until the list ends \
start discounting one from: "discount_req" another random string discounting \
three from: another random string wait until due date by quarter 400')

        simpleNumList.testCurrentToken(
            createDummyTokens(
            total=2, 
            name="req_name test",
            type='start discounting',
            list='CSE 130A, random string until the list ends', 
            due_date = None))

        simpleNumList.testCurrentToken(
            createDummyTokens(
            total=1, 
            name="discount_req", 
            type='discounting',
            list='another random string', 
            due_date = None))

        simpleNumList.testCurrentToken(
            createDummyTokens(
            total=3, 
            name=None, 
            type='by quarter 400',
            list='another random string wait until due date', 
            due_date = 400))



        




if __name__ == "__main__":
    unittest.main()