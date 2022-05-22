#!/usr/bin/python3.9
import parse
from parse import TOKEN_NAME 
from parse import TOKEN_COURSE
from parse import TOKEN_LIST
from parse import TOKEN_DUE_DATE
from parse import TOKEN_COUNT
from parse import TOKEN_TYPE
from parse import TOKEN_PREV_CONCURRENT
from parse import TOKEN_CONCURRENT_LIST
from parse import TOKEN_OP
from parse import TOKEN_EXPR
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

        Return the tokens of the courses 
        'ENVS 23 or CHEM 1A'
        'ENVS 23'
        'CHEM 1A'

        """
        
        def convertToList(expr):
            return list(parse.course_tokens(expr))

        def wrapPreviousTestToNewFormat(tuple_list):
            list = []
            for course, pos in tuple_list:
                if course != 'and' and course != 'or':
                    list.append({TOKEN_COURSE: course})
            return list
                
        self.assertEqual(
            wrapPreviousTestToNewFormat([('ENVS 100', 0), ('and', 9), ('ENVS 100L', 13)]), 
                        convertToList('ENVS 100 and ENVS 100L'))

        self.assertEqual(wrapPreviousTestToNewFormat([('ENVS 183A', 0)]), 
                        convertToList('ENVS 183A'))
        
        self.assertEqual(wrapPreviousTestToNewFormat(
            [('ENVS 24', 0), ('or', 8), ('BIOE 20C', 11)]), 
                        convertToList('ENVS 24 or BIOE 20C'))
    
        self.assertEqual(
            wrapPreviousTestToNewFormat([('ENVS 24', 0), ('or', 8), ('BIOE 20C', 11)]), 
                        convertToList('ENVS 24 or BIOE 20C'))

        self.assertEqual(wrapPreviousTestToNewFormat(
                        [
                        ('STAT 7', 0),
                        ('and', 7),
                        ('STAT 7L', 11),
                        ('or', 20),
                        ('ECON 113', 23),
                        ('or', 32),
                        ('OCEA 90', 35)
                        ]),
                    convertToList('STAT 7 and STAT 7L, or ECON 113 or OCEA 90'))
        


        self.assertEqual(
wrapPreviousTestToNewFormat([('ENVS 100', 0), ('and', 9), ('ENVS 100L', 13)]), 
                        convertToList('ENVS 100 and ENVS 100L'))
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

        def createDummyTokens(expr, total, name, list, type, due_date):
            return {TOKEN_EXPR: expr, TOKEN_COUNT: total, TOKEN_NAME: name, 
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
            expr = 'one from: ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21, PHIL 22, PHIL 24, PHIL 28,\
 or PHIL 80G',
            total=1, 
            name=None, 
            list=
            ['ANTH 2', 'SOCY 1', 'SOCY 10', 'SOCY 15', 'PHIL 21', 'PHIL 22', 
            'PHIL 24', 'PHIL 28', 'PHIL 80G'],
            type=None,
            due_date = None))

        simpleNumList = NumTest(
'two from: "req_name test" CSE 130A, random string until the list ends \
start discounting one from: "discount_req" another random string discounting \
three from: another random string wait until due date by quarter 400')

        simpleNumList.testCurrentToken(
            createDummyTokens(
            expr = 'two from: "req_name test" CSE 130A, random string until the list ends \
start discounting',
            total=2, 
            name="req_name test",
            type='start discounting',
            list=['CSE 130A', 'random string until the list ends'], 
            due_date = None))

        simpleNumList.testCurrentToken(
            createDummyTokens( 
            expr = 'one from: "discount_req" another random string discounting',
            total=1, 
            name="discount_req", 
            type='discounting',
            list=['another random string'], 
            due_date = None))

        simpleNumList.testCurrentToken(
            createDummyTokens(
            expr = 'three from: another random string wait until due date by quarter 400',
            total=3, 
            name=None, 
            type='by quarter 400',
            list=['another random string wait until due date'], 
            due_date = 400))

    def test_reqs_list_tokens(self):
        """
        Given a string of a comma-delimited list whose elements may be
        a list:

        "ECON 101, PHYS 23, (ECON 23 and CSE-101), or MATH 19A"
        returns a result of
        "ECON 101"
        "PHYS 23"
        "(ECON 23 and CSE-101)"
        "MATH 19A"
        """


        tokens = parse.reqs_list_tokens("ANTH 2, SOCY 1, SOCY 10, \
SOCY 15, (ECON 23 and CSE 1), PHIL 21, PHIL 22, PHIL 24, PHIL 28, or PHIL 80G")

        self.assertEqual(next(tokens), 'ANTH 2')
        self.assertEqual(next(tokens), 'SOCY 1')
        self.assertEqual(next(tokens), 'SOCY 10')
        self.assertEqual(next(tokens), 'SOCY 15')
        self.assertEqual(next(tokens), '(ECON 23 and CSE 1)')
        self.assertEqual(next(tokens), 'PHIL 21')
        self.assertEqual(next(tokens), 'PHIL 22')
        self.assertEqual(next(tokens), 'PHIL 24')
        self.assertEqual(next(tokens), 'PHIL 28')
        self.assertEqual(next(tokens), 'PHIL 80G')


        #Even with additional spaces and not needed ors, it should be
        #equivalent
        tokens = parse.reqs_list_tokens("ANTH 2,or  SOCY 1,or SOCY 10, \
or SOCY 15, (ECON 23 and CSE 1), PHIL 21, PHIL 22,   or  PHIL 24, \
PHIL 28, or PHIL 80G")

        self.assertEqual(next(tokens), 'ANTH 2')
        self.assertEqual(next(tokens), 'SOCY 1')
        self.assertEqual(next(tokens), 'SOCY 10')
        self.assertEqual(next(tokens), 'SOCY 15')
        self.assertEqual(next(tokens), '(ECON 23 and CSE 1)')
        self.assertEqual(next(tokens), 'PHIL 21')
        self.assertEqual(next(tokens), 'PHIL 22')
        self.assertEqual(next(tokens), 'PHIL 24')
        self.assertEqual(next(tokens), 'PHIL 28')
        self.assertEqual(next(tokens), 'PHIL 80G')
    
    def test_concurrent_enrollment_tokens(self):
        tokens = parse.concurrent_enrollment_tokens('Previous or concurrent \
enrollment in MATH 3, AM 3, or equivalent, or a mathematics placement score \
of 300 or higher')
        def createDummyTokens(course_list, op=None, allowPrevious=False):
            if op:
                return {TOKEN_CONCURRENT_LIST: course_list, 
                        TOKEN_PREV_CONCURRENT: allowPrevious,
                        TOKEN_OP: op}
            return {TOKEN_CONCURRENT_LIST: course_list, 
                        TOKEN_PREV_CONCURRENT: allowPrevious}
        self.assertDictEqual(next(tokens), createDummyTokens(
            allowPrevious = True,
            course_list = ["MATH 3", "AM 3"]))
        
        tokens = parse.concurrent_enrollment_tokens('concurrent enrollment \
        in PHYS 5L is required.')

        self.assertDictEqual(next(tokens), 
        createDummyTokens(allowPrevious=False, course_list=['PHYS 5L'])
        )

        tokens = parse.concurrent_enrollment_tokens('MATH 24 or \
    previous or concurrent enrollment in AM 20')

        self.assertDictEqual(next(tokens), 
        createDummyTokens(allowPrevious=True, course_list=['AM 20']))
        



        




if __name__ == "__main__":
    unittest.main()