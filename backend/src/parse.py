#!/usr/bin/python3.9
from re import compile
from enumerate import word2int
from req_types import NumFrom

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

or

[Previous or] Concurrent enrollment in TOKEN_LIST [is required]

where portions covered by [] are option and * indicates that it may 
repeat multiple times

"""

#These tokens are identifiers 
TOKEN_DISCOUNTS = 'discounts'
TOKEN_NAME = 'name'
TOKEN_LIST = 'list'
TOKEN_DUE_DATE = 'quarter'
TOKEN_COURSE = 'course_list'
TOKEN_OP = 'op'
TOKEN_COUNT = 'total'
TOKEN_TYPE = 'type'
TOKEN_CONCURRENT = 'concurrent'
TOKEN_CONCURRENT_LIST = 'concurrent_list'
TOKEN_PREV_CONCURRENT = 'prevEnrollAllowed'
TOKEN_MULTIPLE_CONCURRENT = 'multiple'
TOKEN_NUM_FROM = 'num_from'
TOKEN_NUM_FROM_EACH = 'each_list'

TOKEN_REQUIREMENT = 'req'
TOKEN_POS = 'position'
TOKEN_EXPR = 'expr'
TOKEN_RECOMMEND = 'rec'
TOKEN_NO_CREDIT = 'no_credit'
TOKEN_BLACKLIST = 'bkaclist'

#Regex pattern matches responsible for parsing our prerequisites
op = f"(?P<{TOKEN_OP}>(and|or))"
course = f"(?P<{TOKEN_COURSE}>[A-Z]+ *[\d]+[A-Z]?)"
courses_list = compile(f" *(Completion *of *)?{course},? *{op}? *")
nums = f"(?P<{TOKEN_COUNT}>one|two|three|four|five|six|seven|eight|nine|ten)"
req_list_better = f"(?P<{TOKEN_LIST}>(.+?))"
#Modified regex expression from
#https://stackoverflow.com/questions/33400570/regex-to-parse-a-comma-separated-list-excluding-content-within-parentheses
seperate_req_list = compile(
    f" *(?P<{TOKEN_LIST}>[^,(]*(?:\([^)]*\))*[^,]*)(, *or)? *")
types = f"(?P<{TOKEN_TYPE}>(?:start *discounting|discounting|by *quarter\
 *(?P<{TOKEN_DUE_DATE}>\d+)|$))"
num_from = compile(
    f"(?P<{TOKEN_NUM_FROM_EACH}> *{nums} *from: *(\"(?P<{TOKEN_NAME}>.*?)\")? *{req_list_better} *{types} *)"
)
delim = compile(r"(; *and *|\. *|; *(?! *or))")
concurrent_enrollment_list = f"(?P<{TOKEN_CONCURRENT_LIST}>([A-Z]+ *[\d]+[A-Z]?)\
(,? *(and|or)? *[A-Z]+ *[\d]+[A-Z]?)*)"
concurrent_enrollment = compile(
f"(?P<{TOKEN_CONCURRENT}>(?P<{TOKEN_PREV_CONCURRENT}>[pP]revious *or)? *[cC]oncurrent *enrollment *in *\
{concurrent_enrollment_list} *(is *required)? *)"
)
missing_req_list = compile(r"&\s*(?![^()]*\))")

def split(pattern, expr: str):
    """Split a string by an regex expression, and remove any empty
    strings and existing elements that still match our expression
    """
    list = pattern.split(expr)
    for elem in list[:]:
        if elem == '' or pattern.match(expr):
            list.remove(elem)
    return list
def requirements_list(expr: str):
    """Given an string of prerequisites, return a structured list
    of strings that represent the prerequisite.

    Args:
        expr (list): A list of requirements 
    """
    return split(delim, expr)

def missing_requirements(boolean_expr: str):
    """Given an boolean expression representing a missing prerequisite,
    return a structured list that represent what is missing"""
    reqs = []
    replace_tokens = [("&", " and "), ("|", " or "), ("(", ""), (")", "")]
    for expr in split(missing_req_list, boolean_expr):
        for tok, replacement in replace_tokens:
            expr = expr.replace(tok, replacement)
        reqs.append(expr)
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
        yield {TOKEN_COURSE: match[TOKEN_COURSE]}


def num_from_tokens(num_from_expr: str):
    """Returns a stream of dictionary tokens for 
    some arbitrary number of classes that is required from some list.

    Args:
        num_from_expr (str): A string representing a num from expression
        from the following format:

        "num from: Course, Course, Course, or ANY LIST [start 
        discounting num2 from: Course, Course, Course, or ANY LIST] 
        [discounting num3 from: ...]... [by quarter date]


    Yields:
        (Iterable): A stream of requirement list tokens
    """
    for match in num_from.finditer(num_from_expr):
        toks = {}
        components = [TOKEN_COUNT, TOKEN_NAME, TOKEN_DUE_DATE, TOKEN_TYPE]
        for comp in components:
            valid_result = match[comp]
            if valid_result:
                toks[comp] = match[comp]
            else:
                toks[comp] = None

        count = toks[TOKEN_COUNT]
        due_date = toks[TOKEN_DUE_DATE]
        #Convert the token "one" in "one from:" to an integer value
        toks[TOKEN_COUNT] = word2int[count]
        if due_date:
            #Convert the token "6" in "by quarter 6" to an integer value
            toks[TOKEN_DUE_DATE] = int(due_date)
        toks[TOKEN_LIST] = list(reqs_list_tokens(match[TOKEN_LIST]))
        toks[TOKEN_EXPR] = match[TOKEN_NUM_FROM_EACH]
        yield toks

def build_num_from(num_from_expr: str):
    """Due to the num_from expresison being more complex, there exists"""
    num_from_args = {}
    num_from_args[TOKEN_DISCOUNTS] = discounts = []

    each_num_from = num_from_tokens(num_from_expr)

    first_num_from = next(each_num_from)

    num_from_args.update(first_num_from)

    for tok in each_num_from:
        due_date = tok[TOKEN_DUE_DATE]
        discounts.append(NumFrom(**tok))
        if due_date:
            num_from_args[TOKEN_DUE_DATE] = due_date
    yield num_from_args


def reqs_list_tokens(reqs_list: str):
    """Returns a stream of courses that is the list of a "num_from" 
    expression

    Args:
        reqs_list (str): A list of courses following what comes after
        "num from:" 

        Example:

        An "num_from" expression 

        'three from: CSE 101, ECON 104, (MATH 19A and MATH 19B), or
        PHYS 23 by quarter 6'

        would require the inputs of

        'CSE 101, ECON 104, (MATH 19A and MATH 19B), or PHYS 23'

        for this function.
    Yields:
        (Iterable): A stream of courses, either as a course name
        or an boolean expression of courses
    """
    for match in seperate_req_list.finditer(reqs_list):
        course_list = match[TOKEN_LIST]
        if course_list:
            yield course_list
            
def concurrent_enrollment_tokens(conc_enr: str):
    """Returns a stirng of classes that requires concurrent/previous enrollment
    from an concurrent enrollment expression
    

    Args:
        conc_enr (str): A set of classes following the format:
        
        "[Previous or] [cC]oncurent enrollment in COURSE_LIST is required. and/or..."
    Yields:
        (Iterable): A boolean expression of a stream of courses that 
        requires either a single or multiple concurrent enrollments 
    """
    for match in concurrent_enrollment.finditer(conc_enr):
        toks = {}
        allowPrevious = match[TOKEN_PREV_CONCURRENT]
        if allowPrevious:
            toks[TOKEN_PREV_CONCURRENT] = True
        else:
            toks[TOKEN_PREV_CONCURRENT] = False
        course_list = match[TOKEN_CONCURRENT_LIST]
        toks[TOKEN_CONCURRENT_LIST] = course_list
        yield toks

TOKENS_MATCH_FUNCTIONS = {
    TOKEN_COURSE: course_tokens,
    TOKEN_CONCURRENT: concurrent_enrollment_tokens,
    TOKEN_NUM_FROM: build_num_from
}

TOKENS_MATCH_PATTERNS = {
    TOKEN_NUM_FROM: f'(?P<{TOKEN_NUM_FROM}>'+ num_from.pattern +'+)',
    TOKEN_CONCURRENT: concurrent_enrollment.pattern,
    TOKEN_COURSE: course
}

"""
Somethings our regex pattern finds a match that partially looks like
a requirement that is in fact completely irrelevant/optional. We implement
a list of blacklisted patterns that we specifically instruct our program
not to consider them as a requirement.
"""
BLACKLIST_PATTERNS = {
    TOKEN_RECOMMEND: r' *recommended *as *prerequisite *to *this *course *',
    TOKEN_NO_CREDIT: r" *may *not *enroll * in *"
}


extract_requriements = compile(
f' *(,? *{op})? *' +
f'(?P<{TOKEN_REQUIREMENT}>' + '|'.join(TOKENS_MATCH_PATTERNS.values()) + ')'
)

blacklist_requirements = compile(
f'(?P<{TOKEN_BLACKLIST}>' + '|'.join(BLACKLIST_PATTERNS.values()) + ')')

def find_req(match):
    """Given an match, find exactly the tokens of what requirements the match
    exactly corresponds to"""
    for tok, func in TOKENS_MATCH_FUNCTIONS.items():
        req, req_pos = match[tok], match.start(tok)
        if req:
            args = next(func(req))
            args[TOKEN_EXPR] = req
            return token(TOKEN_ID=tok, kwargs=args, 
                        pos=req_pos, expr=req)


def token(TOKEN_ID, kwargs, expr, pos):
    """Abstraction method that specifies what format a token should be
    returned as

    Args:
        TOKEN_ID (str): A token identifier matching the the associated token object
        kwargs (**kwargs): Standard keyword arguments for the token object
        expr (str): The token expression
        pos (int): An integer representing the initial position of the expression
    """
    return TOKEN_ID, kwargs, expr, pos

def parse(expr: str):
    """The main tokenizer function that extracts requirements into the
    neccesary bits and pieces to create our Abstract Syntrax Tree
    """
    for match in extract_requriements.finditer(expr):
        op = match[TOKEN_OP]
        pos = match.start(TOKEN_OP)
        if op:
            yield token(TOKEN_ID=TOKEN_OP, kwargs={TOKEN_OP: op}, pos=pos, expr=op)
        yield find_req(match)

def requirement_found(expr: str):
    """If an requirement is found within our expression, return true.
    Otherwise false.

    Args:
        expr (str): A requirement expression

    Returns:
        boolean: A status indicator for whether a requirement was found
    """
    return extract_requriements.search(expr) is not None and blacklist_requirements.search(expr) is None
