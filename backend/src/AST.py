#!/usr/bin/python3.9
from cgi import parse_multipart
from boolean import BooleanAlgebra
from boolean import TOKEN_NOT
from boolean import TOKEN_AND
from boolean import TOKEN_OR
from boolean import TOKEN_TRUE
from boolean import TOKEN_FALSE
from boolean import TOKEN_LPAR
from boolean import TOKEN_RPAR
from boolean import Expression
from req_types import Course
from req_types import ConcurrentEnrollment
from req_types import NumFrom
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
TRUE, FALSE, NOT, AND, OR, symbol = algebra.definition()
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
                    # An expression that follows ( and / ( or is invalid
                    if self.previous_token == TOKEN_LPAR and tok == TOKEN_OP:
                        yield update_token(TOKEN_FALSE, 'false', self.position)

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


def missing_requirements(parse: Expression):
    """Given an Abstract Syntax Tree parse reprsenting our
    prerequisites, convert this into a string fits more to the format of
    UCSC's prerequisites. 

    Args:
        parse (Expression): An parse object from PrereqAlgebra()

    Returns:
        str: A string of prerequisites
    """
    if parse.isliteral:
        return(str(parse))
    replace_tokens = [("&", " and "), ("|", " or ")]
    missing_reqs = []
    for arg in parse.args:
        arg = str(arg).strip()
        for tok, replacement in replace_tokens:
            arg = arg.replace(tok, replacement)
        missing_reqs.append(arg)
    if parse.pretty().startswith("OR"):
        return "; or ".join(missing_reqs)
    return "; ".join(missing_reqs)