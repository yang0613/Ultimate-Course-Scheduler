#!/usr/bin/python3.9
from boolean import BooleanAlgebra
from boolean import Symbol
from boolean import TOKEN_NOT
from boolean import TOKEN_AND
from boolean import TOKEN_OR
from boolean import TOKEN_TRUE
from boolean import TOKEN_FALSE
from boolean import TOKEN_LPAR
from boolean import TOKEN_RPAR
from enumerate import int2word
from parse import TOKEN_OP
from parse import requirements_list, requirement_found, parse
from parse import TOKEN_COURSE, TOKEN_CONCURRENT, TOKEN_NUM_FROM

TOKENS = { #Standard tokens from Boolean Algebra
            '*': TOKEN_AND, '&': TOKEN_AND, 'and': TOKEN_AND,
            '+': TOKEN_OR, '|': TOKEN_OR, 'or': TOKEN_OR,
            '~': TOKEN_NOT, '!': TOKEN_NOT, 'not': TOKEN_NOT,
            '(': TOKEN_LPAR, ')': TOKEN_RPAR,
            '[': TOKEN_LPAR, ']': TOKEN_RPAR,
            'true': TOKEN_TRUE, '1': TOKEN_TRUE,
            'false': TOKEN_FALSE, '0': TOKEN_FALSE, 'none': TOKEN_FALSE
        }

algebra = BooleanAlgebra(allowed_in_token=('.', ':', '_', '-', '/'))

class Course(Symbol):
    """A variable representing the following format: 
    className classID[optLetter]
    """
    def __init__(self, expr, **kwargs):
        super().__init__(expr)

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
                test_course = algebra.parse(course).subs(substitutions).simplify()
            else:
                test_course = algebra.parse(course).subs(self.quarter).simplify()
            if test_course == algebra.TRUE:
                return algebra.TRUE
            return self
    
    def setQuarterClasses(self, substitution):
        """A helper function for constraint.py to check for concurrent
        enrollment
        """
        self.quarter = substitution

class NumFrom(Symbol):
    """A class representing any Num_From expression
    """
    def __init__(self, expr, name, list, total, discounts=[], quarter=None, **kwargs):
        self.course_list = list
        self.discounts = discounts
        self.total = total
        self.quarter = quarter
        self.name = name
        super().__init__(expr)

    def count(self, substitutions):
        count = 0
        for course in self.course_list:
            test_course = algebra.parse(course).subs(substitutions).simplify()
            if test_course == algebra.TRUE:
                count = count + 1
        for discount in self.discounts:
            count = count + max(discount.total, discount.count(substitutions))
        return count

    def _subs(self, substitutions, default, simplify):
        remaining_class = self.total - self.count(substitutions)
        if remaining_class < 0:
            return algebra.TRUE
        else:
            new_expr = self.expr.replace(int2word[self.total],
            int2word[remaining_class], 1)
            return self.__class__(expr=new_expr,
                                  course_list=self.course_list,
                                  total = remaining_class,
                                  discounts = self.discounts)

TOKENS_MATCH_SYMBOLS = {
    TOKEN_COURSE: Course,
    TOKEN_CONCURRENT: ConcurrentEnrollment,
    TOKEN_NUM_FROM: NumFrom,
    TOKEN_OP: lambda op: TOKENS[op.lower()]
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
        

        requirements = requirements_list(expr)

        for req in requirements:
            if requirement_found(req):
                yield update_token(TOKEN_LPAR, '(', self.position)
                for tok, args, expr, pos in parse(req):
                    req_obj = TOKENS_MATCH_SYMBOLS[tok](**args)
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

