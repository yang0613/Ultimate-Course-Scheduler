
from re import compile


"""
Responsible for parsing a prerequisite string into tokens from the 
following patterns

TOKEN_COUNT from: TOKEN_LIST [discounting TOKEN_COUNT from: TOKEN_LIST]* [by
quarter TOKEN_DUE_DATE]
"one from: ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21, PHIL 22, PHIL 24,
PHIL 28, or PHIL 80G"

or

TOKEN_COURSE [TOKEN_OP TOKEN_COURSE]*
"STAT 7 and STAT 7L, or ECON 113 or OCEA 90"

where portions covered by [] are option and * indicates that it may 
repeat multiple times

"""

#These tokens are identifiers 
TOKEN_DISCOUNTS = 'discounts'
TOKEN_NAME = 'name'
TOKEN_LIST = 'list'
TOKEN_DUE_DATE = 'due_date'
TOKEN_COURSE = 'course'
TOKEN_OP = 'op'
TOKEN_COUNT = 'total'
TOKEN_TYPE = 'type'

#Regex pattern matches responsible for parsing our prerequisites
op = f"(?P<{TOKEN_OP}>(and|or))"
course = f"(?P<{TOKEN_COURSE}>[A-Z]+ *[\d]+[A-Z]?)"
courses_list = compile(f" *(Completion *of *)?{course},? *{op}? *")
nums = f"(?P<{TOKEN_COUNT}>one|two|three|four|five|six|seven|eight|nine|ten)"
req_list_better = f"(?P<{TOKEN_LIST}>(.+?))"
types = f"(?P<{TOKEN_TYPE}>(?:start *discounting|discounting|by *quarter\
 *(?P<{TOKEN_DUE_DATE}>\d+)|$))"
num_from_better = compile(
    f" *{nums} *from: *(\"(?P<{TOKEN_NAME}>.*?)\")? *{req_list_better} *{types} *"
)
delim = compile(r"(; *and *|\. *|; *(?! *or))")

def get_requirements(expr: str):
    """Given an string of prerequisites, return a structured list
    of strings that represent the prerequisite.

    Args:
        expr (list): A list of requirements 
    """
    reqs = delim.split(expr)
    for r in reqs[:]:
        if r == '' or delim.match(r):
            reqs.remove(r)
    return reqs


def course_tokens(course_list: str):
    """Returns a stream of courses by their names and starting character
    positions

    Args:
        course_list (str): A string representing a list of courses
        in the following format:
        
        course (and|or) course[,] (and|or) course[,] ... course

    Yields:
        (Iterable): A stream of course tokens
    """
    for match in courses_list.finditer(course_list):
        course, course_pos = match.group('course'), match.start('course')
        op, op_pos = match.group('op'), match.start('op')
        yield course, course_pos
        if op:
            yield op, op_pos


def num_from_tokens(reqs_list: str):
    """Returns a stream of tokens for some arbitrary number of classes
    is required from some list.

    Args:
        reqs_list (str): A string representing a requirements list in
        the following format:

        "num from: Course, Course, Course, or ANY LIST [start 
        discounting num2 from: Course, Course, Course, or ANY LIST] 
        [discounting num3 from: ...]... [by quarter date]


    Yields:
        (Iterable): A stream of requirement list tokens
    """
    enumerate = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
    'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10 
    }
    for match in num_from_better.finditer(reqs_list):
        toks = {}
        requirements = [TOKEN_COUNT, TOKEN_NAME, TOKEN_LIST, TOKEN_DUE_DATE, TOKEN_TYPE]
        for req in requirements:
            valid_result = match.group(req)
            if valid_result:
                toks[req] = match.group(req)
            else:
                toks[req] = None

        count = toks[TOKEN_COUNT]
        due_date = toks[TOKEN_DUE_DATE]
        #Convert the token "one" in "one from:" to an integer value
        toks[TOKEN_COUNT] = enumerate[count]
        if due_date:
            #Conver the token "6" in "by quarter 6" to an integer value
            toks[TOKEN_DUE_DATE] = int(due_date)
        yield toks
