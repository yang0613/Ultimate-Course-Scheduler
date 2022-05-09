
from boolean import BooleanAlgebra
from boolean import Symbol
from boolean import TOKEN_NOT
from boolean import TOKEN_AND
from boolean import TOKEN_OR
from boolean import TOKEN_TRUE
from boolean import TOKEN_FALSE
from boolean import TOKEN_SYMBOL
from boolean import TOKEN_LPAR
from boolean import TOKEN_RPAR
from re import match
from re import split
from re import finditer
from re import compile

"""
THIS IS WIP CODE, BY NO MEANS IS IT NEAR DONE
"""
list_class = r" *(Completion *of *)?(?P<course>[A-Z]+ *[\d]+[A-Z]?),? *(?P<op>(and|or)?) *"
list = compile(r" *(Completion *of *)?(?P<course>[A-Z]+ *[\d]+[A-Z]?),? *(?P<op>(and|or)?) *")
req_list = r" *(?P<total>one|two|three|four|five|six|seven|eight|nine|ten) *from: *(\"(?P<req_name>.*?)\")? *(?P<req_list>([A-Z]+ *[\d]+[A-Z]?,? *(and|or)? *)+) *(?P<discounts>(discounting (one|two|three|four|five|six|seven|eight|nine|ten) *from: *(\".*?\")? *([A-Z]+ *[\d]+[A-Z]?,? *(and|or)? *)* *)*)"
one_from = "test"
regexs = [list_class]        
delim = r"(; *and *|\. *|; *(?! *or))"
TOKENS = { #Standard tokens from Boolean Algebra
            '*': TOKEN_AND, '&': TOKEN_AND, 'and': TOKEN_AND,
            '+': TOKEN_OR, '|': TOKEN_OR, 'or': TOKEN_OR,
            '~': TOKEN_NOT, '!': TOKEN_NOT, 'not': TOKEN_NOT,
            '(': TOKEN_LPAR, ')': TOKEN_RPAR,
            '[': TOKEN_LPAR, ']': TOKEN_RPAR,
            'true': TOKEN_TRUE, '1': TOKEN_TRUE,
            'false': TOKEN_FALSE, '0': TOKEN_FALSE, 'none': TOKEN_FALSE
        }

class Course(Symbol):
    """A variable representing the following format: 
    className classID[optLetter]
    """

def token_list(expr):
    position = 1
    for m in list.finditer(expr):
        course, course_pos = m.group('course'), m.start('course')
        op, op_pos = m.group('op'), m.start('op')
        position += course_pos
        yield Course(course), course, position
        if op != '':
            position += course_pos
            yield TOKENS[op.lower()], op, position

class PrereqAlgebra(BooleanAlgebra):


    def __init__(self):
        self.position = 0
        super().__init__(allowed_in_token=',')

    def tokenize(self, expr):
        
        def process_reqs(expr):
            reqs = split(delim, expr)
            for r in reqs[:]:
                if r == '' or match(delim, r):
                    reqs.remove(r)
            return reqs

        requirements = process_reqs(expr)
        print(requirements)
        for req in requirements:
            if list.match(req):
                yield TOKEN_LPAR, '(', self.position
                self.position += 1
                for COURSE_OBJ, course_name, pos in token_list(req):
                    self.position += pos
                    yield COURSE_OBJ, course_name, self.position
                yield TOKEN_RPAR, ')', self.position
                self.position += 1
            else:    
                yield Symbol(req), req, self.position
                self.position += 1
            yield TOKEN_AND, 'and', self.position
            self.position += 1
    
    
            """
                               
                for m in finditer(list_class, req):
                    course = m.group('course')
                    yield Course(course), course, self.position
                    self.position += 1
                    op = m.group('op')
                    if op !=  '':
                        print(op)
                        yield TOKENS[op.lower()], op, self.position
                        self.position += 1
                yield TOKEN_RPAR, ')', self.position
                self.position += 1
                yield TOKEN_AND, 'and', self.position
                self.position += 1
            """

splitter = r"(\.|;(?! *or))"
#print(algebra.parse("This or is or a or  requirement or The or other or one").get_symbols())

test = PrereqAlgebra()

expr = "ENVS 23 or CHEM 1A; ENVS 24 or BIOE 20C; ENVS 25; and STAT 7 and STAT 7L, or ECON 113 or OCEA 90; and one from: ANTH 2, SOCY 1, SOCY 10, SOCY 15, PHIL 21, PHIL 22, PHIL 24, PHIL 28, or PHIL 80G. Concurrent enrollment in ENVS 100L Is required."

parsed = test.parse(expr)
print(parsed.pretty())
print(parsed)
expr2 = "AM 3 or AM 6, or MATH 3 or higher; or mathematics placement examination (MPE) score of 300 or higher; or AP Calculus AB exam score of 3 or higher; ENVS 23 recommended as prerequisite to this course."
test_str =" and     test"
test2 = BooleanAlgebra(allowed_in_token=',')
expr2 = "STAT 7 and STAT 7L, or ECON 113 or OCEA 90; ENVS 24."
p2 = test.parse(expr2)
expr3 = "((STAT_7 and STAT_7L) or ECON_113 or OCEA_90) and (ENVS_24)"
p3 = BooleanAlgebra().parse(expr3)
expr4 = "STAT 7 and STAT 7L, or ECON 113 or OCEA 90"
expr5 = "CSE 104, ECON 104, or ECON 104"
#out = test.parse(expr5)
for tok in token_list(expr5):
    print(tok)
#print(p2.pretty())
#print(out.pretty())

