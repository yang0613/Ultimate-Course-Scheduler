from boolean import Symbol
from enumerate import int2word
import AST
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
        algebra = AST.algebra
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
        algebra = AST.algebra
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
        algebra = AST.algebra
        count = 0
        for course in self.course_list:
            test_course = algebra.parse(course).subs(substitutions).simplify()
            if test_course == algebra.TRUE:
                print(course)
                count = count + 1
        for discount in self.discounts:
            count = count + min(discount.total, discount.count(substitutions))
        return count

    def _subs(self, substitutions, default, simplify):
        algebra = AST.algebra
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