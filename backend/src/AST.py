#!/usr/bin/python3.9
from boolean import BooleanAlgebra
from boolean import TOKEN_NOT
from boolean import TOKEN_AND
from boolean import TOKEN_OR
from boolean import TOKEN_TRUE
from boolean import TOKEN_FALSE
from boolean import TOKEN_LPAR
from boolean import TOKEN_RPAR
from boolean import Expression
from boolean import Symbol
from boolean import Symbol
from enumerate import int2word
import parse


TOKENS = { #Standard tokens from Boolean Algebra
            '*': TOKEN_AND, '&': TOKEN_AND, 'and': TOKEN_AND,
            '+': TOKEN_OR, '|': TOKEN_OR, 'or': TOKEN_OR,
            '~': TOKEN_NOT, '!': TOKEN_NOT, 'not': TOKEN_NOT,
            '(': TOKEN_LPAR, ')': TOKEN_RPAR,
            '[': TOKEN_LPAR, ']': TOKEN_RPAR,
            'true': TOKEN_TRUE, '1': TOKEN_TRUE,
            'false': TOKEN_FALSE, '0': TOKEN_FALSE, 'none': TOKEN_FALSE
        }



class PrereqAlgebra(BooleanAlgebra):
    """An AST implementation for a specific prerequisite.
    """

    def __init__(self):
        super().__init__(allowed_in_token=',')


    def tokenize(self, expr):

        self.position = 0
        self.previous_token = None, '', 0

        def update_token(TOKEN, str, pos):
            """Saves the latest token in history and update our 
            positioning in the tokens
            """
            self.previous_token = TOKEN
            if pos == self.position:
                self.position = self.position + 1
            return TOKEN, str, pos
        

        requirements = parse.requirements_list(expr)

        for req in requirements:
            if parse.requirement_found(req):
                yield update_token(TOKEN_LPAR, '(', self.position)
                for tok, args, expr, pos in parse.parse(req):
                    # An expression that follows ( and / ( or is invalid
                    req_obj = TOKENS_MATCH_SYMBOLS[tok](**args)
                    if self.previous_token == TOKEN_LPAR:
                        if req_obj == TOKEN_OR:
                            yield update_token(TOKEN_FALSE, 'false', self.position)
                        elif req_obj == TOKEN_AND:
                            yield update_token(TOKEN_TRUE, 'true', self.position)

                    yield update_token(req_obj, expr, self.position+pos)

                ##Check to see for unbalanced operators from our regex
                ##expression. When every possible requirement is encountered
                ##for, no unbalanced operators will occur and these yields 
                ##will never run
                if self.previous_token == TOKEN_OR:
                    yield update_token(TOKEN_FALSE, 'false', self.position)
                elif self.previous_token == TOKEN_AND:
                    yield update_token(TOKEN_TRUE, 'true', self.position)
                
                yield update_token(TOKEN_RPAR, ')', self.position)
                yield update_token(TOKEN_AND, 'and', self.position)
        #Required since "ANDs" require dual operators
        yield update_token(TOKEN_TRUE, 'true', self.position)

algebra = PrereqAlgebra()

class Course(Symbol):
    """A variable representing the following format: 
    className classID[optLetter]
    """
    def __init__(self, expr, **kwargs):
        self.expr = expr
        super().__init__(expr)
    
    def _subs(self, substitutions, default, simplify):
        if self.expr in substitutions.keys():
            return substitutions[self.expr]

class ConcurrentEnrollment(Symbol):
    """A class representing a Concurrent Enrollment requirement in our
    AST
    """
    def __init__(self, expr, concurrent_list, prevEnrollAllowed):
        self.expr = expr
        self.concurrent_list = concurrent_list
        self.prevEnrollAllowed = prevEnrollAllowed
        super().__init__(expr)

    def _subs(self, substitutions, default, simplify):
        for course in self.concurrent_list:
            if self.prevEnrollAllowed:
                all_classes = substitutions | self.quarter
                test_course = algebra.parse(course).subs(all_classes).simplify()
            else:
                test_course = algebra.parse(course).subs(self.quarter).simplify()
            if test_course == algebra.TRUE:
                return algebra.TRUE
        return self
    
    def setQuarterClasses(self, classes):
        """A helper function for constraint.py to check for concurrent
        enrollment
        """
        subs = {}
        for course in classes:
            subs[course] = algebra.TRUE
        self.quarter = subs

class NumFrom(Symbol):
    """A class representing any Num_From expression
    """
    def __init__(self, expr, name, list, total, discounts=[], quarter=None, **kwargs):
        self.course_list = list
        self.discounts = discounts
        self.total = total
        self.quarter = quarter
        self.name = name
        self.expr = expr
        if self.name:
            #Temporarily remove the list from the expression
            #because the expression's list can be very long and
            #cloud up the results
            self.expr = self.expr_without_list()
        super().__init__(expr)

    def expr_without_list(self):
        """Returns the expression without the list
        From "one from: "NumFrom name" COURSE 1A, COURSE1B, or COURSE 3A
        to "one from: "NumFrom name"
        """
        return f"{int2word[self.total]} from: \"{self.name}\""

    def count(self, substitutions):
        count = 0
        for course in self.course_list:
            test_course = algebra.parse(course).subs(substitutions).simplify()
            if test_course == algebra.TRUE:
                count = count + 1
        for discount in self.discounts:
            count = count + min(discount.total, discount.count(substitutions))
        return count

    def _subs(self, substitutions, default, simplify):
        remaining_class = self.total - self.count(substitutions)
        if remaining_class <= 0:
            return algebra.TRUE
        else:
            new_expr = self.expr.replace(int2word[self.total],
            int2word[remaining_class], 1)
            return self.__class__(expr=new_expr,
                                  name=self.name,
                                  list=self.course_list,
                                  total = remaining_class,
                                  discounts = self.discounts)

TOKENS_MATCH_SYMBOLS = {
    parse.TOKEN_COURSE: Course,
    parse.TOKEN_CONCURRENT: ConcurrentEnrollment,
    parse.TOKEN_NUM_FROM: NumFrom,
    parse.TOKEN_OP: lambda op: TOKENS[op.lower()],
    parse.TOKEN_PAR: lambda expr: TOKENS[expr.lower()]
}


def split_ast(parse: Expression):
    """Given an Abstract Syntax Tree parse object,
    split the tree at depth 1 into a list 

    Args:
        parse (Expression): An parse object

    Returns:
        str: A list representation of our AST
    """
    if parse.isliteral:
        return([str(parse)])
    replace_tokens = [("&", " and "), ("|", " or ")]
    arg_list = []
    for arg in parse.args:
        arg = str(arg).strip()
        for tok, replacement in replace_tokens:
            arg = arg.replace(tok, replacement)
        arg_list.append(arg)
    return arg_list

def missing_requirements(parse: Expression):
    """Given an Abstract Syntax Tree parse reprsenting our
    prerequisites, convert this into a string fits more to the format of
    UCSC's prerequisites. 

    Args:
        parse (Expression): An parse object from PrereqAlgebra()

    Returns:
        str: A string of prerequisites
    """
    missing_reqs = split_ast(parse)
    if parse.pretty().startswith("OR"):
        return "; or ".join(missing_reqs)
    return missing_reqs


def convert_schedule(schedule):
    """Convert's a JSON schedule into an subsitution dictionary mapping
    following boolean.py specifications

    Args:
        schedule (JSON): JSON Object holding our Schedule

    Returns:
        A dictionary of symbols with an substituted value TRUE
    """
    subs = {}
    for year, quarter, classes in parse.schedule_tokens(schedule):
        for course in classes:
            subs[course] = algebra.TRUE
    return subs