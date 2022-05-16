from boolean import Symbol
from enumerate import int2word
from boolean import BooleanAlgebra

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